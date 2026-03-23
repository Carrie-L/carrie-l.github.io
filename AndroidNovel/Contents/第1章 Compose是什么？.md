---
chapter_id: '1'
title: '第一课： Compose 是什么？'
official_url: 'https://developer.android.com/compose'
status: 'draft'
author: 'minimax m2.5 - OpenClaw'
plot_summary:
  time: '早晨'
  location: '卧室'
  scene: '主角醒来，发现手机里多了一个神秘App'
  season: '春季'
  environment: '清晨的阳光'
---

# 第一课： Compose 是什么？

---

“叮——”

清晨的阳光透过窗帘的缝隙，洒在林小满的脸上。她揉了揉眼睛，发现手机屏幕上弹出了一个陌生的应用图标——那是一个由蓝色和绿色组成的奇怪符号，下面写着四个字：“ Compose 之书”。

“这是什么？我什么时候下载的？”

她戳了一下图标，屏幕突然闪出一道炫目的光芒。等光芒散去，她发现自己不在床上了。

---

## 陌生的世界

“小满！起来了！”

林小满睁开眼，发现自己站在一片草地上。天空是澄澈的蓝色，远處传来鸟鸣声和溪水的流淌声。她的身上穿着一件奇怪的白色长袍，手里还拿着——一台笔记本电脑？

“这里是……哪里？”她喃喃自语。

“这里是 Compose 村！”一个清脆的声音从身后传来。

林小满转过身，看到一个扎着马尾辫的少女，正笑眯眯地看着她。少女大约十七八岁，手里拿着一根……画笔？

“你是谁？”林小满警惕地问。

“我叫 Compose 精灵，你可以叫我小 Com！”少女眨了眨眼，“你是被选中的开发者，来这里学习 Jetpack Compose 的！”

“Jetpack……Compose？”林小满一脸茫然。

---

## Compose 是什么？

小 Com 笑着在空中挥了一下画笔，空气中突然出现了一幅画面——那是一个手机界面，上面有图片、文字、按钮，看起来像一个 App。

“所谓 Jetpack Compose，”
小 Com 解释道，
“就是 Android 的现代 UI 工具包。简单来说——”

她又一挥画笔，画面变成了一堆代码：

```kotlin
@Composable
fun Greeting(name: String) {
    Text(text = "Hello, $name!")
}
```

“以前写 Android UI，需要写一堆 XML，然后再写一堆 Java 或 Kotlin 代码把它们关联起来。”小 Com 说，“但有了 Compose，你只需要用 Kotlin 代码，就能直接描述界面长什么样。”

“就像……画出来一样？”林小满问。

“没错！”小 Com 打了个响指，“Compose 的核心理念就是：**用 Kotlin 写 UI，UI 即代码，代码 即 UI**。”

---

## 为什么用 Compose？

林小满开始感兴趣了：“那……它比以前的写法好吗？”

“好问题！”小 Com 开始列举：

| 传统写法 | Compose 写法 |
|---------|-------------|
| XML + View 系统 | 纯 Kotlin |
| 需要findViewById | 自动状态管理 |
| 手动更新 UI | 声明式 UI |
| 代码量大 | 代码量少 50%+ |

“而且，”小 Com 压低声音，故作神秘地说，“Compose 是 Google 官方推荐的未来。现在学，就是走在时代前沿！”

---

## 第一个 Compose 程序

“好啦，别光说不动。”小 Com 拉起林小满的手，“我带你去做第一个 Compose 程序！”

她们来到一间小木屋，里面有一张桌子，桌上放着一台电脑“。

打开 Android Studio，”小 Com 说，“我们新建一个项目。”

林小满照做了。屏幕上出现了项目创建的向导。

“选择 'Empty Views Activity' 还是 'Empty Compose Activity'？”她问。

“选 Compose！选 Compose！”小 Com 兴奋地说。

选择完成后，Android Studio 自动生成了一段代码：

```kotlin
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            Greeting("Android")
        }
    }
}

@Composable
fun Greeting(name: String) {
    Text(text = "Hello $name!")
}
```

“这就是一个最简单的 Compose 程序！”小 Com 解释道，“`setContent` 里面的 lambda，就是你界面的根节点。`Text` 是一个Composable 函数，用来显示文字。”

林小满似懂非懂地点了点头。

---

## 本课小结

这一天，林小满在 Compose 村里学到了第一课：

1. **Jetpack Compose** 是 Android 的现代 UI 工具包
2. 用 **Kotlin** 直接写 UI，代码即界面
3. **声明式** 编程，状态驱动 UI 变化
4. Google 官方推荐，是 Android 开发的未来

---

“今天就到这里吧！”小 Com 伸了个懒腰，“明天我们学点更有意思的——怎么在 Compose 里显示图片！”

“等等……”林小满还没来得及问怎么回去，眼前的画面就开始模糊了。

“明天见，小满！”

---

*”叮——“*

林小满猛地睁开眼睛，发现自己还在床上。手机屏幕亮着，那个奇怪的 App 图标还在。

原来是一场梦？

她戳开那个图标，屏幕上出现了四个字：

**“明天再见”**

---

### 📚 课后练习

1. 下载 Android Studio，创建第一个 Compose 项目
2. 尝试修改 `Greeting` 函数，把 `“Hello $name!”` 改成别的文字
3. 在屏幕上再加一个 `Text`，显示你的名字

---

**下集预告**：第二章 · 显示图片 · Image 组件详解
