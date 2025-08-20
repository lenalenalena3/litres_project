import allure
from allure_commons.types import AttachmentType

USE_SELENOID = False


def add_screenshot(browser):
    png = browser.driver.get_screenshot_as_png()
    allure.attach(body=png, name='screenshot', attachment_type=AttachmentType.PNG, extension='.png')


def add_logs(browser):
    try:
        if USE_SELENOID:
            logs = browser.driver.execute("getLog", {"type": 'browser'})["value"]
        else:
            logs = browser.driver.get_log('browser')
        log_text = "\n".join(str(log) for log in logs)
    except Exception as e:
        log_text = f"Логи недоступны: {e}"
    allure.attach(log_text, 'browser_logs', AttachmentType.TEXT, extension='.log')


def add_html(browser):
    html = browser.driver.page_source
    allure.attach(body=html, name='page_source', attachment_type=AttachmentType.HTML, extension='.html')


def add_xml(browser):
    xml = browser.driver.page_source
    allure.attach(body=xml, name='xml', attachment_type=AttachmentType.XML, extension='.xml')


def add_video(browser, url):
    video_url = f"https://{url}/video/{browser.driver.session_id}.mp4"
    html = "<html><body><video width='100%' height='100%' controls autoplay><source src='" \
            + video_url \
            + "' type='video/mp4'></video></body></html>"
    allure.attach(html, 'video_' + browser.driver.session_id, AttachmentType.HTML, '.html')
