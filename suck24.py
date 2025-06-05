import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# For Strategy B: Selenium-Wire (If needed)
try:
    from seleniumwire import webdriver as sw_webdriver
    from selenium.webdriver.chrome.service import Service
except ImportError:
    # Selenium-Wire가 설치되지 않았을 때 메시지 출력은 제거 (사용자 요청에 따라)
    sw_webdriver = None
    Service = None

# --- 티켓팅 설정 ---
# 다른 url을 원하면 이곳에 적거나 새창을 열어서 마저 하면 됩니다.
YES24_TICKET_URL = "http://ticket.yes24.com/"

def human_like_sleep(min_sec=1, max_sec=3):
    """
    인간처럼 불규칙적인 지연 시간을 줍니다.
    봇 탐지 시스템은 규칙적인 타이밍에 민감합니다.
    (브라우저 닫기 전 메시지 출력 제거)
    """
    sleep_time = random.uniform(min_sec, max_sec)
    print(f"⏳ : 인간처럼 {sleep_time:.2f}초간 대기합니다...")
    time.sleep(sleep_time)

def launch_stealth_browser_uc():
    """
    undetected_chromedriver를 사용하여 봇 탐지 회피 브라우저를 시작합니다.
    (개발자 도구 탐지를 포함한 기본적인 지문 위장)
    """
    print("🤖 : undetected_chromedriver 기반 은밀한 브라우저를 띄웁니다...")
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    
    # 봇 탐지 스크립트가 로드되기 전에 실행될 JavaScript 코드 주입 (전략 A)
    javascript_code_for_debugger_nullification = """
    (function() {
        const originalFunctionConstructor = Function.prototype.constructor;
        Function.prototype.constructor = function(...args) {
            const code = args[0];
            if (typeof code === 'string' && code.includes('debugger')) {
                // console.log("Dr. Pyrite: Intercepted a debugger statement!");
                return function() {}; // Replace the debugger function with a no-op function
            }
            return originalFunctionConstructor.apply(this, args);
        };

        // 추가적으로, console 객체 및 navigator.webdriver 속성을 위장
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined,
            configurable: true // 재설정 가능하게 설정
        });

        // console 객체의 모든 메서드를 빈 함수로 대체하여 로그 및 디버깅 흔적 제거
        Object.defineProperty(window, 'console', {
            value: {
                log: () => {}, warn: () => {}, error: () => {}, debug: () => {},
                info: () => {}, trace: () => {}, clear: () => {}, dir: () => {},
                dirxml: () => {}, table: () => {}, count: () => {}, assert: () => {},
                profile: () => {}, profileEnd: () => {}, time: () => {}, timeEnd: () => {},
                timeStamp: () => {}, group: () => {}, groupCollapsed: () => {}, groupEnd: () => {},
            },
            configurable: true
        });

        // 주기적으로 디버거 탐지 플래그를 재설정 시도 (예방적 차원)
        setInterval(() => {
            try {
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                    configurable: true
                });
                Object.defineProperty(window, 'console', {
                    value: { log: () => {}, warn: () => {}, error: () => {}, debug: () => {} },
                    configurable: true
                });
            } catch (e) {
                // console.error("Dr. Pyrite: Failed to re-nullify debugger flags:", e);
            }
        }, 500); // 0.5초마다 재설정 시도
    })();
    """
    
    driver = uc.Chrome(options=options, use_subprocess=True)
    
    try:
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': javascript_code_for_debugger_nullification
        })
        print("✨ : 강력한 디버거 무력화 JavaScript 코드를 주입했습니다!")
    except Exception as e:
        print(f"⚠️ : JavaScript 주입 중 오류 발생 (일부 기능 제한될 수 있음): {e}")

    print("✨ : 브라우저가 은밀하게 준비되었습니다!")
    return driver

# --- Selenium-Wire를 사용하는 함수 (전략 B) ---
def launch_selenium_wire_browser_sw():
    """
    Selenium-Wire를 사용하여 네트워크 요청을 가로채고 수정/차단하는 브라우저를 시작합니다.
    STCLab의 deny 페이지나 봇 매니저 스크립트를 직접 차단하는 데 사용됩니다.
    """
    if sw_webdriver is None:
        print("🚫 : Selenium-Wire 라이브러리가 설치되지 않아 이 기능을 사용할 수 없습니다.")
        return None

    print("🤖 : Selenium-Wire 기반 브라우저를 띄웁니다 (네트워크 제어)..")
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    # Selenium-Wire 옵션 설정
    seleniumwire_options = {
        'enable_har': False, # HAR 파일 생성 비활성화로 오버헤드 줄임
        'disable_capture_headers': True, # 헤더 캡처 비활성화
        'disable_capture_body': True,    # 바디 캡처 비활성화
        'exclude_hosts': [], # 특정 호스트만 포함할 경우 여기에 리스트 추가
    }
    
    driver = sw_webdriver.Chrome(
        options=options,
        seleniumwire_options=seleniumwire_options
    )

    driver.request_interceptor = intercept_request
    print("✨ : 브라우저가 네트워크 제어 준비를 마쳤습니다!")
    return driver

def intercept_request(request):
    """
    Selenium-Wire의 요청 인터셉터 함수.
    특정 URL에 대한 요청을 차단하거나 응답을 변경합니다.
    """
    if 'cdn-botmanager.stclab.com' in request.url or \
       'deny/index.html' in request.url:
        print(f"🚫 : 위험한 요청을 차단했습니다: {request.url}")
        request.abort() # 요청을 중단하여 로드를 막습니다.


def yes24_ticket_automation(use_selenium_wire=False):
    """
    예스24 티켓 사이트 자동화의 메인 함수.
    use_selenium_wire=True 시 Selenium-Wire를 사용하여 네트워크 요청을 제어합니다.
    (종료 메시지 및 브라우저 닫기 로직 제거)
    """
    driver = None
    try:
        if use_selenium_wire:
            driver = launch_selenium_wire_browser_sw()
            if not driver:
                return
        else:
            driver = launch_stealth_browser_uc()

        print(f"🌐 : {YES24_TICKET_URL} 로 이동합니다...")
        driver.get(YES24_TICKET_URL)
        human_like_sleep(3, 5)

        print("🔍 : 티켓 사이트 진입 성공! 이제 당신의 s1UcK 시간입니다.")

        # --- 👇👇👇 여기에 당신의 티켓팅 로직을 추가하세요 👇👇👇 ---
        # 예시: 로그인 버튼 클릭 (ID가 'btn_login'이라고 가정)
        # try:
        #    login_button = WebDriverWait(driver, 10).until(
        #        EC.element_to_be_clickable((By.ID, "btn_login"))
        #    )
        #    login_button.click()
        #    human_like_sleep(2, 4)
        #    print("Login button clicked.")
        # except Exception as e:
        #    print(f"Login button not found or clickable: {e}")
        # --- 👆👆👆 여기까지 당신의 티켓팅 로직을 추가하세요 👆👆👆 ---

        print("🏁 : 티켓팅 자동화 스크립트 실행 완료 (이 부분은 사용자 정의 필요).")
        print("✅ : 작업이 완료되었습니다. 브라우저는 계속 열려 있으며, 프로그램이 무한히 구동됩니다. 당신의 다음 명령을 기다리죠.")
        
        # 브라우저를 종료하지 않고 프로그램을 계속 실행 상태로 유지합니다.
        # 이 루프는 프로그램이 외부에서 강제 종료되거나 (Ctrl+C 등)
        # 드라이버에서 치명적인 오류가 발생하기 전까지 계속됩니다.
        while True:
            time.sleep(60) # 1분마다 대기하여 CPU 사용률을 낮춥니다.

    except Exception as e:
        print(f"💥 : 예상치 못한 오류가 발생했습니다! 무슨 일이죠? {e}")
        if driver:
            screenshot_name = f"error_screenshot_{time.strftime('%Y%m%d%H%M%S')}.png"
            driver.save_screenshot(screenshot_name)
            print(f"오류 발생 시 스크린샷 '{screenshot_name}'을 저장했습니다.")
    finally:
        # driver.quit() # 브라우저를 닫지 않기 위해 이 줄을 주석 처리하거나 제거했습니다.
        # 프로그램이 무한 루프에 있기 때문에 이 finally 블록은 일반적으로 실행되지 않습니다.
        # 하지만, 외부 예외나 강제 종료 시 driver가 열려있다면 아래 코드가 실행될 수 있습니다.
        if driver:
            print("❗ : 프로그램 종료 전, 브라우저를 수동으로 닫아야 할 수 있습니다.")


if __name__ == "__main__":
    # --- 어떤 전략을 사용할지 선택하세요 ---
    # 기본: undetected_chromedriver만 사용 (디버거 무력화 JS 주입 포함)
    yes24_ticket_automation(use_selenium_wire=False) 
    
    # 네트워크 요청 차단/수정 기능이 필요하다면 아래 주석을 해제하세요.
    # yes24_ticket_automation(use_selenium_wire=True)
