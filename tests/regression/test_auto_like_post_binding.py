from __future__ import annotations

import shutil
import unittest

from instagram_tools.auto_like_browser import PlaywrightFollowingFeed


class _DomSession:
    def __init__(self, page):
        self.page = page

    def _require_page(self):
        return self.page

    @staticmethod
    def raise_browser_error(exc):
        raise exc


class StablePostBindingRegressionTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            from playwright.sync_api import sync_playwright
        except ImportError as exc:
            raise unittest.SkipTest("playwright is not installed") from exc

        executable = (
            shutil.which("google-chrome")
            or shutil.which("google-chrome-stable")
            or shutil.which("chromium")
            or shutil.which("chromium-browser")
        )
        if not executable:
            raise unittest.SkipTest("Chrome/Chromium is not installed")

        cls._playwright = sync_playwright().start()
        cls._browser = cls._playwright.chromium.launch(headless=True, executable_path=executable)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, "_browser"):
            cls._browser.close()
        if hasattr(cls, "_playwright"):
            cls._playwright.stop()

    def setUp(self):
        self.page = self._browser.new_page(viewport={"width": 900, "height": 900})
        self.session = _DomSession(self.page)

    def tearDown(self):
        self.page.close()

    @staticmethod
    def _article(shortcode: str, *, sponsored: bool = False) -> str:
        marker = "<span>Sponsored</span>" if sponsored else ""
        return f"""
        <article data-post="{shortcode}">
          <header><a href="/{shortcode}/">friend</a>{marker}</header>
          <a href="/p/{shortcode}/"><div class="media"></div></a>
          <section>
            <button aria-label="Like"
              onclick="this.setAttribute('aria-label', 'Unlike')"></button>
            <button aria-label="Comment"></button>
            <button aria-label="Share Post"></button>
          </section>
        </article>
        """

    def test_posts_remain_bound_to_permalink_when_article_indexes_shift(self):
        self.page.set_content(
            "<style>article{width:620px;min-height:120px}.media{height:40px}</style>"
            + self._article("first")
            + self._article("ad", sponsored=True)
            + self._article("next")
        )
        feed = PlaywrightFollowingFeed(self.session)
        posts = list(feed.posts())

        self.assertEqual([post.key for post in posts], ["/p/first/", "/p/ad/", "/p/next/"])

        # Instagram mutates/virtualizes the feed while auto-like is processing.
        # Inserting an article above the snapshot used to shift every live
        # locator.nth(index), so the ad decision for one key was applied to its
        # neighbor instead.
        self.page.evaluate(
            """html => {
                const wrapper = document.createElement('div');
                wrapper.innerHTML = html;
                document.body.insertBefore(wrapper.firstElementChild, document.body.firstChild);
            }""",
            self._article("inserted"),
        )

        self.assertEqual(posts[1].exclusion_reason, "sponsored")
        self.assertIsNone(posts[2].exclusion_reason)

        self.assertTrue(posts[2].click_like())
        self.assertEqual(
            self.page.locator('article:has(a[href="/p/next/"]) button[aria-label="Unlike"]').count(),
            1,
        )
        self.assertEqual(
            self.page.locator('article:has(a[href="/p/ad/"]) button[aria-label="Like"]').count(),
            1,
        )


if __name__ == "__main__":
    unittest.main()
