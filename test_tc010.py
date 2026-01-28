from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 测试TC010：新增场地 - 创建后跳转
def test_tc010():
    # 初始化Chrome浏览器
    driver = webdriver.Chrome()
    
    try:
        # 1. 访问登录页面
        driver.get("http://localhost:3000/")
        driver.maximize_window()
        
        # 2. 登录系统
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "username")))
        
        driver.find_element(By.NAME, "username").send_keys("admin")
        driver.find_element(By.NAME, "password").send_keys("admin123")
        driver.find_element(By.TAG_NAME, "button").click()
        
        # 3. 等待跳转到首页
        WebDriverWait(driver, 20).until(EC.url_contains("/home"))
        
        # 4. 导航到场地管理页面
        driver.get("http://localhost:3000/admin/venues")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), '场地管理')]")))
        
        # 5. 点击"新增场地"按钮
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), '新增场地')]")))
        driver.find_element(By.XPATH, "//button[contains(text(), '新增场地')]").click()
        
        # 6. 等待跳转到新增场地页面
        WebDriverWait(driver, 20).until(EC.url_contains("/admin/venues/add"))
        
        # 7. 填写表单
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "name")))
        
        driver.find_element(By.NAME, "name").send_keys("测试场地TC010")
        driver.find_element(By.NAME, "code").send_keys("test_venue_010")
        driver.find_element(By.NAME, "address").send_keys("北京市朝阳区测试地址")
        
        # 8. 提交表单
        driver.find_element(By.XPATH, "//button[contains(text(), '保存')]").click()
        
        # 9. 验证是否跳转到场地详情页面
        WebDriverWait(driver, 20).until(EC.url_contains("/admin/venues/detail"))
        
        print("TC010 测试成功：新增场地后跳转成功")
        
    except Exception as e:
        print(f"TC010 测试失败：{str(e)}")
    finally:
        # 关闭浏览器
        driver.quit()

if __name__ == "__main__":
    test_tc010()
