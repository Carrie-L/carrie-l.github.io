---
chapter_id: '8'
title: '第八课：TextField 输入框 · 表单与验证'
official_url: 'https://developer.android.com/compose.foundation.text'
status: 'done'
author: 'minimax m2.5 - OpenClaw'
plot_summary:
  time: '第八天'
  location: 'Compose 村·邮局'
  scene: '小 Com 教小满填表单'
  season: '春季'
  environment: '温暖的邮局，里面有各种表格'
---

# 第八课：TextField 输入框 · 表单与验证

---

“叮——”

林小满发现自己站在一家邮局里。柜台上堆满了各种表格和信封。

“今天我们要学习填表！”小 Com 拿着一叠表格走了过来，“在 Compose 里，输入框是最重要的表单组件——TextField！”

“输入框我会啊，”林小满说，“不就是 TextField 吗？”

“那你可能只学会了皮毛！”小 Com 笑道，“TextField 有很多高级用法，比如密码框、多行文本、输入验证……学会这些，才能做出好用的表单！”

---

## 第一个 TextField

“先从最基本的开始。”小 Com 打开电脑：

```kotlin
var text by remember { mutableStateOf("") }

OutlinedTextField(
    value = text,
    onValueChange = { text = it },
    label = { Text("请输入文字") }
)
```

“`value` 是输入框的内容，`onValueChange` 是内容变化时的回调。”小 Com 解释。

---

## TextField vs OutlinedTextField

“Compose 提供了两种输入框样式：”

| 组件 | 样式 | 适用场景 |
|------|------|----------|
| `TextField` | 填充样式 | Material 3 默认 |
| `OutlinedTextField` | 边框样式 | 需要明显边界 |

```kotlin
// 填充样式
TextField(value = text, onValueChange = { text = it })

// 边框样式
OutlinedTextField(value = text, onValueChange = { text = it })
```

---

## 常用属性

“TextField 有很多属性。”小 Com 列举：

```kotlin
OutlinedTextField(
    value = text,
    onValueChange = { text = it },
    
    // 标签
    label = { Text("用户名") },
    placeholder = { Text("请输入用户名") },
    
    // 辅助文字
    supportingText = { Text("至少6个字符") },
    
    // 前缀/后缀
    prefix = { Text("+86 ") },
    suffix = { Text("@email.com") },
    
    // 图标
    leadingIcon = { Icon(Icons.Default.Person, "用户") },
    trailingIcon = { Icon(Icons.Default.Close, "清空") },
    
    // 形状
    shape = RoundedCornerShape(12.dp),
    
    // 颜色
    colors = OutlinedTextFieldDefaults.colors(
        focusedBorderColor = Color.Blue,
        unfocusedBorderColor = Color.Gray
    ),
    
    // 只读
    readOnly = false,
    
    // 启用
    enabled = true
)
```

---

## 密码框

“密码框需要用 `visualTransformation`。”小 Com 展示了代码：

```kotlin
var password by remember { mutableStateOf("") }
var passwordVisible by remember { mutableStateOf(false) }

OutlinedTextField(
    value = password,
    onValueChange = { password = it },
    label = { Text("密码") },
    visualTransformation = if (passwordVisible)
        VisualTransformation.None
    else
        PasswordVisualTransformation(),
    trailingIcon = {
        IconButton(onClick = { passwordVisible = !passwordVisible }) {
            Icon(
                if (passwordVisible) Icons.Default.VisibilityOff
                else Icons.Default.Visibility,
                contentDescription = if (passwordVisible) "隐藏密码" else "显示密码"
            )
        }
    }
)
```

---

## 多行文本

“如果要输入多行文本，比如评论，该怎么做？”小 Com 问。

```kotlin
var comment by remember { mutableStateOf("") }

OutlinedTextField(
    value = comment,
    onValueChange = { comment = it },
    label = { Text("评论") },
    minLines = 3,
    maxLines = 5
)
```

| 属性 | 用途 |
|------|------|
| `minLines` | 最小行数 |
| `maxLines` | 最大行数（超过可滚动） |
| `textStyle` | 文字样式 |

---

## 输入限制：VisualTransformation

“有时候需要限制输入内容，比如只能输入数字。”小 Com 展示了：

```kotlin
// 只允许输入数字
OutlinedTextField(
    value = text,
    onValueChange = { newText ->
        text = newText.filter { it.isDigit() }
    }
)

// 手机号格式化
val phoneNumberFormatter = remember { PhoneNumberFormatter() }
OutlinedTextField(
    value = phone,
    onValueChange = { phone = phoneNumberFormatter.format(it) },
    visualTransformation = { trans ->
        PhoneNumberTransformation()
    }
)

// 信用卡号格式化
val creditCardFormatter = remember { CreditCardFormatter() }
```

---

## 表单验证

“在真实应用中，输入框通常需要验证。”小 Com 展示了验证逻辑：

```kotlin
var email by remember { mutableStateOf("") }
var emailError by remember { mutableStateOf<String?>(null) }

OutlinedTextField(
    value = email,
    onValueChange = {
        email = it
        emailError = null  // 清除错误
    },
    label = { Text("邮箱") },
    isError = emailError != null,
    supportingText = emailError?.let { { Text(it, color = Color.Red) } }
)

// 验证函数
fun validateEmail(email: String): String? {
    return when {
        email.isBlank() -> "邮箱不能为空"
        !email.contains("@") -> "邮箱格式不正确"
        !email.contains(".") -> "邮箱格式不正确"
        else -> null
    }
}

// 提交时验证
Button(onClick = {
    emailError = validateEmail(email)
}) {
    Text("提交")
}
```

---

## 实战：完整注册表单

“我们来做最后一个练习——一个完整的注册表单！”小 Com 提议道。

```kotlin
@Composable
fun RegisterForm() {
    var username by remember { mutableStateOf("") }
    var email by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    var confirmPassword by remember { mutableStateOf("") }
    var agreeTerms by remember { mutableStateOf(false) }
    
    var usernameError by remember { mutableStateOf<String?>(null) }
    var emailError by remember { mutableStateOf<String?>(null) }
    var passwordError by remember { mutableStateOf<String?>(null) }
    
    Column Modifier
            .fillMaxWidth()
            .padding(16(
        modifier =.dp)
    ) {
        // 用户名
        OutlinedTextField(
            value = username,
            onValueChange = {
                username = it
                usernameError = null
            },
            label = { Text("用户名") },
            isError = usernameError != null,
            supportingText = usernameError?.let { { Text(it, color = Color.Red) } },
            leadingIcon = { Icon(Icons.Default.Person, null) },
            modifier = Modifier.fillMaxWidth(),
            shape = RoundedCornerShape(12.dp)
        )
        
        Spacer(modifier = Modifier.height(12.dp))
        
        // 邮箱
        OutlinedTextField(
            value = email,
            onValueChange = {
                email = it
                emailError = null
            },
            label = { Text("邮箱") },
            isError = emailError != null,
            supportingText = emailError?.let { { Text(it, color = Color.Red) } },
            leadingIcon = { Icon(Icons.Default.Email, null) },
            modifier = Modifier.fillMaxWidth(),
            shape = RoundedCornerShape(12.dp)
        )
        
        Spacer(modifier = Modifier.height(12.dp))
        
        // 密码
        OutlinedTextField(
            value = password,
            onValueChange = {
                password = it
                passwordError = null
            },
            label = { Text("密码") },
            isError = passwordError != null,
            supportingText = passwordError?.let { { Text(it, color = Color.Red) } },
            leadingIcon = { Icon(Icons.Default.Lock, null) },
            visualTransformation = PasswordVisualTransformation(),
            modifier = Modifier.fillMaxWidth(),
            shape = RoundedCornerShape(12.dp)
        )
        
        Spacer(modifier = Modifier.height(12.dp))
        
        // 确认密码
        OutlinedTextField(
            value = confirmPassword,
            onValueChange = { confirmPassword = it },
            label = { Text("确认密码") },
            leadingIcon = { Icon(Icons.Default.Lock, null) },
            visualTransformation = PasswordVisualTransformation(),
            modifier = Modifier.fillMaxWidth(),
            shape = RoundedCornerShape(12.dp)
        )
        
        Spacer(modifier = Modifier.height(16.dp))
        
        // 同意条款
        Row(
            verticalAlignment = Alignment.CenterVertically
        ) {
            Checkbox(
                checked = agreeTerms,
                onCheckedChange = { agreeTerms = it }
            )
            Text("我同意服务条款", style = MaterialTheme.typography.bodyMedium)
        }
        
        Spacer(modifier = Modifier.height(24.dp))
        
        // 注册按钮
        Button(
            onClick = {
                // 验证
                usernameError = if (username.length < 3) "用户名至少3个字符" else null
                emailError = if (!email.contains("@")) "邮箱格式不正确" else null
                passwordError = if (password.length < 6) "密码至少6个字符" else null
                
                if (usernameError == null && emailError == null && passwordError == null && agreeTerms) {
                    // 提交表单
                }
            },
            modifier = Modifier
                .fillMaxWidth()
                .height(56.dp),
            shape = RoundedCornerShape(12.dp),
            enabled = agreeTerms
        ) {
            Text("注册", style = MaterialTheme.typography.titleMedium)
        }
    }
}
```

---

## 键盘类型

“还可以控制键盘类型，让用户体验更好。”小 Com 补充：

```kotlin
OutlinedTextField(
    value = text,
    onValueChange = { text = it },
    keyboardOptions = KeyboardOptions(
        keyboardType = KeyboardType.Email,  // 邮箱键盘
        imeAction = ImeAction.Done  // 完成按钮
    ),
    keyboardActions = KeyboardActions(
        onDone = { /* 提交 */ }
    )
)
```

| KeyboardType | 用途 |
|---------------|------|
| `Text` | 普通文本 |
| `Email` | 邮箱 |
| `Password` | 密码 |
| `Phone` | 手机号 |
| `Number` | 数字 |
| `Uri` | URL |

---

## 本课小结

今天林小满学到了：

1. **TextField / OutlinedTextField**：两种输入框样式
2. **常用属性**：label / placeholder / icon / supportingText
3. **密码框**：visualTransformation 实现
4. **多行文本**：minLines / maxLines
5. **输入限制**：filter 过滤字符
6. **表单验证**：isError / supportingText
7. **键盘控制**：KeyboardOptions

---

“表单太有用了！”林小满说，“几乎每个 App 都需要！”

“没错！”小 Com 说，“学会表单，你就能做登录、注册、设置页面了！”

“明天我们学什么？”

“明天学——导航！”小 Com 笑道，“多页面应用的实现！”

---

*”叮——“*

手机通知：**“第八章 已解锁：TextField 输入框”**

---

### 📚 课后练习

1. 做一个登录页面，包含用户名和密码
2. 做一个评论输入框，支持多行
3. 做一个带实时验证的表单

---

**下集预告**：第九课 · Navigation 导航 · 多页面应用
