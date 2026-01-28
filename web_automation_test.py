from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

# 测试结果记录
results = []

# 启动浏览器
driver = webdriver.Chrome()
driver.maximize_window()
driver.implicitly_wait(10)

try:
    # 登录系统
    print("正在登录系统...")
    driver.get("http://localhost:3000/")
    
    # 输入用户名密码
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "username"))).send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("admin123")
    driver.find_element(By.TAG_NAME, "button").click()
    
    # 等待登录成功，跳转到首页
    WebDriverWait(driver, 20).until(EC.url_contains("/home"))
    print("登录成功！")
    
    # 导航到场地管理页面
    print("正在导航到场地管理页面...")
    driver.get("http://localhost:3000/admin/venues")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), '场地管理')]")))
    print("进入场地管理页面成功！")
    
    # TC010 - 新增场地 - 创建后跳转
    print("\n测试 TC010 - 新增场地 - 创建后跳转")
    try:
        # 点击新增按钮
        driver.find_element(By.XPATH, "//button[contains(text(), '+ 新增场地')]").click()
        
        # 填写表单
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "name"))).send_keys("测试场地跳转")
        driver.find_element(By.NAME, "code").send_keys("test_jump")
        driver.find_element(By.NAME, "address").send_keys("北京市朝阳区跳转测试")
        
        # 点击下一步
        driver.find_element(By.XPATH, "//button[contains(text(), '下一步')]").click()
        
        # 点击确认创建
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), '确认创建')]"))).click()
        
        # 等待创建成功提示
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), '创建成功')]")))
        print("创建场地成功！")
        
        # 点击返回列表
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), '返回列表')]"))).click()
        
        # 验证是否返回列表页
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), '场地管理')]")))
        print("返回列表页成功！")
        
        results.append({"用例ID": "TC010", "测试结果": "通过", "备注": "新增场地后跳转功能正常"})
    except Exception as e:
        print(f"TC010 测试失败: {e}")
        results.append({"用例ID": "TC010", "测试结果": "失败", "备注": str(e)})
    
    # TC018 - 编辑场地 - 取消操作
    print("\n测试 TC018 - 编辑场地 - 取消操作")
    try:
        # 找到第一个场地的编辑按钮并点击
        edit_buttons = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//button[contains(text(), '编辑')]")))
        if edit_buttons:
            edit_buttons[0].click()
            
            # 修改场地名称
            name_input = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "name")))
            original_name = name_input.get_attribute("value")
            name_input.clear()
            name_input.send_keys("修改测试")
            
            # 点击取消
            driver.find_element(By.XPATH, "//button[contains(text(), '取消')]").click()
            
            # 验证是否关闭弹窗
            time.sleep(2)
            # 检查弹窗是否存在
            try:
                driver.find_element(By.XPATH, "//div[contains(@class, 'el-dialog')]")
                print("取消操作失败，弹窗未关闭")
                results.append({"用例ID": "TC018", "测试结果": "失败", "备注": "取消操作后弹窗未关闭"})
            except NoSuchElementException:
                print("取消操作成功，弹窗已关闭")
                results.append({"用例ID": "TC018", "测试结果": "通过", "备注": "取消操作功能正常"})
        else:
            print("未找到编辑按钮")
            results.append({"用例ID": "TC018", "测试结果": "失败", "备注": "未找到编辑按钮"})
    except Exception as e:
        print(f"TC018 测试失败: {e}")
        results.append({"用例ID": "TC018", "测试结果": "失败", "备注": str(e)})
    
    # TC030 - 页面刷新 / 回退
    print("\n测试 TC030 - 页面刷新 / 回退")
    try:
        # 进入新增场地页面
        driver.find_element(By.XPATH, "//button[contains(text(), '+ 新增场地')]").click()
        
        # 填写部分字段
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "name"))).send_keys("刷新测试")
        
        # 刷新页面
        print("正在刷新页面...")
        driver.refresh()
        
        # 验证页面是否正常加载
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), '场地管理')]")))
        print("页面刷新后正常加载！")
        
        # 再次进入新增页面
        driver.find_element(By.XPATH, "//button[contains(text(), '+ 新增场地')]").click()
        
        # 浏览器回退
        print("正在执行浏览器回退...")
        driver.back()
        
        # 验证是否返回列表页
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), '场地管理')]")))
        print("浏览器回退后正常！")
        
        results.append({"用例ID": "TC030", "测试结果": "通过", "备注": "页面刷新和回退功能正常"})
    except Exception as e:
        print(f"TC030 测试失败: {e}")
        results.append({"用例ID": "TC030", "测试结果": "失败", "备注": str(e)})
    
finally:
    # 关闭浏览器
    driver.quit()
    
    # 打印测试结果
    print("\n=================== 测试结果汇总 ===================")
    for result in results:
        print(f"用例ID: {result['用例ID']}, 测试结果: {result['测试结果']}, 备注: {result['备注']}")
    print("==================================================")
