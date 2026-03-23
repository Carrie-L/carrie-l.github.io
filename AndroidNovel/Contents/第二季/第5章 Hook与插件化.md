---
chapter_id: '5'
title: '第五课：Hook 与插件化 · 动态修改 Android 系统'
official_url: 'https://github.com/LSPosed/LSPosed'
status: 'done'
<parameter name="author">'minimax m2.5 - OpenClaw'
plot_summary:
  time: '第三十天'
  location: 'Compose 村·改装车间'
  scene: '小 Com 教小满用 Hook 修改系统行为'
  season: '春季'
  environment: '改装车间里各种工具'
---

# 第五课：Hook 与插件化 · 动态修改 Android 系统

---

“叮——”

林小满发现自己站在一个改装车间里。各种汽车零件散落在地上。

“今天我们要学 Hook 和插件化！”小 Com 拿着工具箱走了过来，“学会这个，就能修改任何 App 的行为！”

“Hook？”林小满问。

“对！”小 Com 说，“Hook 就是'钩子'，能拦截系统调用，修改行为！”

---

## 1. Hook 是什么？

“Hook 是修改系统行为的技术。”小 Com 介绍了：

**Hook 的用途**：
- ✅ 修改系统函数
- ✅ 劫持网络请求
- ✅ 绕过签名验证
- ✅ 自动化测试
- ✅ 插件化框架

---

## 2. Hook 原理

“Hook 的原理是这样的。”小 Com 展示了：

**原理**：
1. 找到目标函数地址
2. 修改函数入口
3. 跳转到我们的代码
4. 执行完后跳转回去

```
原始函数：
┌─────────────────┐
│  函数入口       │───► 原始逻辑
└─────────────────┘

Hook 后：
┌─────────────────┐
│ 我们的代码入口   │───► 自定义逻辑
└─────────────────┘      │
      │                   ▼
      └───────► 原始逻辑 ──► 返回
```

---

## 3. Xposed 框架

“Xposed 是最著名的 Hook 框架。”小 Com 展示了：

```kotlin
// Xposed 模块
class MyHook : IXposedHookLoadPackage {
    override fun handleLoadPackage(lpparam: XC_LoadPackage.LoadPackageParam) {
        if (lpparam.packageName == "com.android.systemui") {
            // Hook SystemUI
            XposedHelpers.findAndHookMethod(
                "com.android.systemui.statusbar.StatusBar",
                lpparam.classLoader,
                "makeStatusBarView",
                object : XC_MethodHook() {
                    override fun afterHookedMethod(param: MethodHookParam) {
                        // 修改 StatusBar
                    }
                }
            )
        }
    }
}
```

---

## 4. LSPosed

“LSPosed 是更新的 Hook 框架。”小 Com 介绍了：

**LSPosed 特点**：
- ✅ 基于 ART
- ✅ 更稳定
- ✅ 支持 SandHook、YAHFA
- ✅ 模块化设计

```kotlin
// LSPosed 模块
@HookAnnotation
class MyHook @Inject constructor(
    @MethodHookParam(HookGroup("System")) param: MethodHookParam
) {
    companion object {
        @Inject
        lateinit var hook: MyHook
    }
    
    @HookMethod
    fun beforeHookedMethod(param: MethodHookParam) {
        // Hook 逻辑
    }
}
```

---

## 5. Hook 示例：绕过签名验证

“我们来看一个实际例子。”小 Com 展示了：

```kotlin
// 绕过签名验证
class SignatureBypass : IXposedHookLoadPackage {
    override fun handleLoadPackage(lpparam: XC_LoadPackage.LoadPackageParam) {
        XposedHelpers.findAndHookMethod(
            "android.content.pm.PackageManager",
            lpparam.classLoader,
            "getPackageInfo",
            String::class.java,
            Int::class.javaPrimitiveType,
            object : XC_MethodHook() {
                override fun beforeHookedMethod(param: MethodHookParam) {
                    val flags = param.args[1] as Int
                    if (flags and PackageManager.GET_SIGNATURES != 0) {
                        // 移除签名检查标志
                        param.args[1] = flags and PackageManager.GET_SIGNATURES.inv()
                    }
                }
            }
        )
    }
}
```

---

## 6. 插件化是什么？

“插件化是动态加载 APK 的技术。”小 Com 介绍了：

**插件化用途**：
- ✅ App 插件化（微信小程序）
- ✅ 热更新
- ✅ 模块化
- ✅ 免安装运行

---

## 7. 插件化框架

“常用的插件化框架。”小 Com 展示了：

| 框架 | 特点 |
|------|------|
| RePlugin | 360 出品，稳定 |
| VirtualAPK | 滴滴出品 |
| Shadow | 腾讯出品 |
| OpenAtlas | 阿里开源 |

---

## 8. 简单插件化实现

“我们来实现一个简单插件化。”小 Com 展示了：

```kotlin
class PluginManager(context: Context) {
    
    private val pluginClassLoader: ClassLoader
    
    fun loadPlugin(pluginPath: String): Boolean {
        return try {
            // 1. 加载插件 APK
            val pluginFile = File(pluginPath)
            val dexPathList = DexPathList(null, pluginFile.absolutePath)
            
            // 2. 创建 ClassLoader
            pluginClassLoader = PathClassLoader(
                pluginFile.absolutePath,
                context.classLoader.parent
            )
            
            true
        } catch (e: Exception) {
            false
        }
    }
    
    fun startPluginActivity(pluginPackage: String) {
        // 启动插件 Activity
        val intent = Intent().apply {
            component = ComponentName(pluginPackage, "com.plugin.MainActivity")
        }
        context.startActivity(intent)
    }
}
```

---

## 9. Hook + 插件化实战

“Hook + 插件化可以做大事！”小 Com 展示了：

```kotlin
class VirtualPluginHook : IXposedHookLoadPackage {
    override fun handleLoadPackage(lpparam: XC_LoadPackage.LoadPackageParam) {
        // 1. Hook Activity 的启动
        XposedHelpers.findAndHookMethod(
            "android.app.ActivityThread",
            lpparam.classLoader,
            "performLaunchActivity",
            ActivityThread.ActivityClientRecord::class.java,
            Intent::class.java,
            object : XC_MethodHook() {
                override fun afterHookedMethod(param: MethodHookParam) {
                    val record = param.args[0] as ActivityThread.ActivityClientRecord
                    val intent = param.args[1] as Intent
                    
                    // 2. 检查是否是插件 Activity
                    if (isPluginIntent(intent)) {
                        // 3. 替换 ClassLoader
                        val activity = param.result
                        val pluginActivity = loadPluginActivity(intent)
                        param.result = pluginActivity
                    }
                }
            }
        )
    }
}
```

---

## 10. 实战：制作 Xposed 模块

“我们来制作一个 Xposed 模块！”小 Com 提议道。

**步骤**：

1. **创建 Android 项目**
2. **添加 Xposed 依赖**
3. **编写 Hook 代码**
4. **配置 xposed_init**
5. **打包安装**

```kotlin
// xposed_init
package com.example.myhook

class MyHookModule : IXposedHookLoadPackage {
    override fun handleLoadPackage(lpparam: XC_LoadPackage.LoadPackageParam) {
        // Hook 逻辑
    }
}
```

```xml
<!-- AndroidManifest.xml -->
<application>
    <meta-data
        android:name="xposedmodule"
        android:value="true" />
    <meta-data
        android:name="xposedminversion"
        android:value="89" />
    <meta-data
        android:name="xposeddescription"
        android:value="我的第一个 Hook 模块" />
</application>
```

---

## 本课小结

今天林小满学到了：

1. **Hook 原理**：拦截和修改
2. **Xposed**：经典 Hook 框架
3. **LSPosed**：现代 Hook 框架
4. **Hook 示例**：实际应用
5. **插件化**：动态加载 APK
6. **插件化框架**：常用方案
7. **简单实现**：插件化原理
8. **实战**：制作 Hook 模块

---

“Hook 和插件化太高级了！”林小满说。

“没错！”小 Com 说，“学会这些，你就能修改任何 App！”

---

*”叮——“*

手机通知：**“第二季第五章 已解锁：Hook 与插件化”**

---

**下集预告**：第六课 · 逆向工程基础 · 分析 APK
