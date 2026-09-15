# Instagram Tools

로컬 Chrome 세션을 이용해 반복적인 Instagram 계정 관리 작업을 보조하는 데스크톱 앱입니다.

이 프로젝트는 Instagram Private API 전체를 포크해 유지하는 대신, 실제 데스크톱 앱에 필요한 브라우저 자동화와 계정 관리 기능만 유지합니다.

## 기능

- 팔로잉 시간순 피드에서 아직 좋아요하지 않은 일반 게시물 처리
- 광고 및 추천 게시물 제외
- 팔로워/팔로잉 비교와 미팔로워 목록 표시
- 사용자가 선택한 계정만 언팔로우
- 언팔로우 후 실제 `following=false` 상태 확인
- 하나의 전용 Chrome 프로필과 로그인 세션 공유
- 활동 제한 신호 감지 시 후속 자동화 중단
- Windows 및 Apple Silicon/Intel macOS 빌드

## 실행

Python 3.11 이상과 Google Chrome이 필요합니다.

```bash
python -m pip install -e .
python -m instagram_tools
```

설치 후에는 다음 명령으로 사용할 수 있습니다.

```bash
instagram-tools
```

앱에는 Instagram 아이디나 비밀번호를 입력하지 않습니다. 처음 실행 시 전용 Chrome 창에서 직접 로그인하며 로그인 상태는 로컬 전용 Chrome 프로필에 저장됩니다.

## 패키지 경계

외부 진입점은 `instagram_tools` 하나입니다.

- `instagram_tools.auto_like`: 팔로잉 피드 자동 좋아요 도메인
- `instagram_tools.non_followers`: 미팔로워 검토 및 선택적 언팔로우 도메인
- `instagram_tools.storage`: 설정과 로컬 데이터 저장소
- `python -m instagram_tools`: 데스크톱 앱 실행

런타임 구현과 외부 진입점 모두 `instagram_tools` 패키지 안에 있습니다.

## 데이터 호환성

새 설치는 제품 이름에 맞는 데이터 디렉터리를 사용합니다.

- Windows: `%LOCALAPPDATA%\\InstagramTools`
- macOS: `~/Library/Application Support/InstagramTools`
- Linux: `${XDG_DATA_HOME:-~/.local/share}/instagram-tools`

기존 `FollowingAutoLiker` 데이터가 있으면 로그인 세션을 자동으로 옮기지 않고 기존 위치를 계속 사용합니다. 새 `InstagramTools` 위치에 설정 또는 실제 Chrome profile 데이터가 생긴 뒤에는 새 위치를 우선합니다. 따라서 실패한 초기화가 빈 새 폴더만 남겨도 기존 로그인 상태를 가리지 않습니다.

## 테스트

```bash
python -m unittest discover -v -s tests/regression -p 'test_*.py'
```

CI에서는 lint/format, import 및 공개 API smoke test, 전체 회귀 테스트 discovery, 1366×768 GUI layout test를 수행한 뒤 Windows와 두 macOS 아키텍처용 앱을 빌드합니다.

## 설계 원칙

이 프로젝트는 대량 성장 자동화 도구보다 **검증 가능한 계정 관리 도구**를 지향합니다. 상태를 변경하는 작업은 가능한 경우 사용자 선택 → 실행 → 사후 상태 확인 → 로컬 로그의 흐름을 유지합니다.

## 위험 및 제한

이 앱은 Meta의 공식 계정 관리 API가 아니라 로그인된 Instagram 웹 세션과 내부 웹 인터페이스를 사용합니다. Instagram 변경에 따라 기능이 중단될 수 있으며 활동 제한, 본인 확인, 로그인 만료 또는 계정 제한이 발생할 수 있습니다. 계정 안전이나 장기 호환성을 보장하지 않습니다.

## 출처와 라이선스

이 프로젝트는 `Daviswhistle/instagrapi` 포크에서 분리되었습니다. 포함된 `instagrapi` 유래 코드와 고지에는 해당 MIT 라이선스 조건을 유지합니다.
