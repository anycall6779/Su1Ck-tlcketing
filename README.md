# Su1Ck-tlcketing

```
티켓 자동화 스크립트 (봇 탐지 회피 & 브라우저 유지)

```
이 Python 스크립트는 Selenium을 기반으로 YES24 티켓팅과 같은 웹 자동화를 수행하며, 
봇 탐지를 회피하고 브라우저를 종료하지 않고 계속 구동시키는 데 초점을 맞춥니다.

### 주요 기능

1.  **봇 탐지 회피 (undetected_chromedriver)**
    * `undetected_chromedriver`를 사용하여 `navigator.webdriver` 속성 숨기기 등 일반적인 Selenium 탐지 징후를 우회합니다.
    * 개발자 도구의 `debugger` 문 무력화 및 `console` 객체 위장 등 강력한 JavaScript 코드를 브라우저에 주입하여 봇 탐지 시스템을 속입니다.
    * `navigator.webdriver` 및 `console` 객체를 주기적으로 재설정하여 지속적인 방어 기능을 제공합니다.

2.  **네트워크 요청 제어 (Selenium-Wire)**
    * `selenium-wire`를 사용하여 특정 봇 관리 시스템(예: `cdn-botmanager.stclab.com`, `deny/index.html`)과 관련된 네트워크 요청을 가로채고 차단할 수 있습니다. (선택 사항)

3.  **인간적인 행동 모방**
    * `random.uniform`을 사용하여 불규칙적인 지연 시간을 도입, 규칙적인 봇 동작 패턴을 피합니다.

4.  **브라우저 자동 종료 방지**
    * 스크립트 실행 완료 후에도 브라우저가 자동으로 닫히지 않고 계속 열린 상태를 유지하며, 프로그램 자체도 무한 루프를 통해 구동을 멈추지 않습니다. 이를 통해 사용자가 열린 브라우저에서 상태를 확인하거나 수동 작업을 이어갈 수 있습니다.

### 사용 방법

1.  **필수 라이브러리 설치:**
    ```bash
    pip install selenium undetected-chromedriver selenium-wire
    ```
    *`selenium-wire`는 선택 사항이지만, 사용하려면 설치해야 합니다.*

2.  **스크립트 실행:**
    * 기본적으로 `undetected_chromedriver`를 사용하여 브라우저가 실행되고 YES24 티켓 페이지로 이동합니다.
    ```python
    python your_script_name.py
    ```
    * `selenium-wire`를 사용하여 네트워크 요청 제어 기능을 활성화하려면 스크립트 하단의 `if __name__ == "__main__":` 블록에서 `yes24_ticket_automation(use_selenium_wire=True)`를 주석 해제하고 실행합니다.

3.  **나만의 티켓팅 로직 추가:**
    * 스크립트 내 `yes24_ticket_automation` 함수 안에 `--- 👇👇👇 여기에 당신의 티켓팅 로직을 추가하세요 👇👇👇 ---` 및 `--- 👆👆👆 여기까지 당신의 티켓팅 로직을 추가하세요 👆👆👆 ---` 주석 사이에 로그인, 공연 선택, 좌석 선택 등의 자동화 코드를 작성하세요.

**주의:**
* 이 스크립트는 웹 자동화 연구 및 학습 목적으로 제공됩니다.
* 웹사이트의 정책 및 약관을 준수하여 사용하시기 바랍니다.

```
