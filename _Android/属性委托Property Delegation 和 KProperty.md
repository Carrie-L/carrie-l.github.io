---
layout: article
title: "属性委托Property Delegation 和 KProperty"
date: 2025-03-06
permalink: /android/shu-xing-wei-tuo-property-delegation-he-kproperty/
tags: ["Kotlin", "Android"]
---

 
## 属性委托

### 简单解释

#### 什么是属性委托？
属性委托就是让一个属性（比如变量）的“工作”交给另一个对象去做。你不用自己管它的细节，交给一个“助手”就行。

#### 怎么用？
用`by`关键字。比如：
```kotlin
var name: String by 助手对象()
```
这里的`助手对象()`会负责`name`的读取和写入。

#### 举个例子
想象你有个`age`属性，想在它变化时打印消息：
```kotlin
import kotlin.properties.Delegates

class Person {
    var age: Int by Delegates.observable(0) { _, 旧值, 新值 ->
        println("年龄从 $旧值 变成 $新值")
    }
}

fun main() {
    val person = Person()
    person.age = 10  // 打印 "年龄从 0 变成 10"
    person.age = 20  // 打印 "年龄从 10 变成 20"
}
```
`Delegates.observable`是Kotlin自带的助手，它会在`age`变化时帮你做事。

#### 另一个例子：延迟加载
`lazy` 用于延迟初始化属性。确保属性在第一次被访问时才进行初始化，后续访问直接返回缓存的值：
```kotlin
class Example {
    val lazyProperty: String by lazy {
        println("初始化 lazyProperty")
        "Hello, World!"
    }
}

fun main() {
    val example = Example()
    println(example.lazyProperty)  // 输出 "初始化 lazyProperty" 和 "Hello, World!"
    println(example.lazyProperty)  // 仅输出 "Hello, World!"（不再初始化）
}
```

### Kotlin的属性委托是什么？

Kotlin的**属性委托**（Property Delegation）是一种特性，允许将属性的 `getter` 和 `setter` 操作委托给另一个对象，而不是在类中直接实现这些操作。这种机制通过 `by` 关键字实现，使得属性的行为可以重用公共逻辑，从而避免在多个类中重复编写相似的代码。

属性委托不仅可以应用于类的属性，还可以用于局部变量，是 Kotlin 中提高代码简洁性和可维护性的重要工具。

---

#### **工作原理**

在 Kotlin 中，属性委托的核心是通过一个委托对象来管理属性的访问行为。委托对象需要实现特定的方法：

- 对于**只读属性**（`val`），委托对象必须实现 `getValue` 方法，提供属性的值。
- 对于**可变属性**（`var`），委托对象需要同时实现 `getValue` 和 `setValue` 方法，分别处理值的读取和写入。

当代码访问或修改属性时，Kotlin 会自动调用委托对象的对应方法。例如：

```kotlin
import kotlin.properties.Delegates

class Example {
    var property: String by Delegates.observable("Initial value") { prop, old, new ->
        println("${prop.name} 从 $old 变为 $new")
    }
}

fun main() {
    val example = Example()
    println(example.property)  // 输出 "Initial value"
    example.property = "New value"  // 输出 "property 从 Initial value 变为 New value"
}
```

在这个例子中，`Delegates.observable` 是一个内置的委托，它在属性值变化时触发回调函数。

#### **自定义委托**

开发者也可以创建自定义委托，通过实现 `getValue` 和 `setValue` 方法来定义属性的行为。以下是一个简单的自定义委托示例：

```kotlin
import kotlin.reflect.KProperty

class Delegate {
    operator fun getValue(thisRef: Any?, property: KProperty<*>): String {
        return "委托的值：${property.name}"
    }

    operator fun setValue(thisRef: Any?, property: KProperty<*>, value: String) {
        println("设置 ${property.name} 为 $value")
    }
}

class Example {
    var property: String by Delegate()
}

fun main() {
    val example = Example()
    println(example.property)  // 输出 "委托的值：property"
    example.property = "新值"  // 输出 "设置 property 为 新值"
}
```

在这个例子中，`Delegate` 类控制了 `property` 属性的读取和写入逻辑。

#### **应用场景**

属性委托在许多场景中都非常有用，例如：

1. **延迟加载**：如 `lazy` 委托，用于在需要时才初始化属性。
2. **观察者模式**：如 `Delegates.observable`，在属性变化时执行特定操作。
3. **依赖注入**：将属性的初始化逻辑交给外部对象。
4. **代码复用**：通过委托实现通用的属性行为，避免重复代码。

#### **优点与注意事项**

**优点**：
- **减少样板代码**：将属性逻辑封装在委托对象中，重用性高。
- **提升可读性**：代码更简洁，关注点分离更清晰。

**注意事项**：
- **避免过度使用**：复杂的委托逻辑可能使代码难以理解。
- **性能考虑**：某些委托（如 `lazy`）可能引入额外的开销，应根据需求权衡使用。

---

### observable

`Delegates.observable()`是Kotlin标准库中的一个内置委托（delegate）。它与**观察者设计模式**（Observer Design Pattern）密切相关。

观察者模式的核心概念是允许一个对象（称为被观察者）维护一组依赖于它的对象（称为观察者），并在其状态发生变化时自动通知所有观察者。这种模式在当多个对象需要被告知某个值发生变化时非常有用，避免了每个依赖对象都需要定期检查资源是否更新的无效操作。

`observable()`接收两个参数：初始值和一个**监听器处理程序**（listener handler），该处理程序在值被修改时会被调用。

当你调用`observable()`时，它会创建一个`ObservableProperty`对象。每当这个委托的setter被调用时，传递给它的lambda（即监听器处理程序）都会执行。这种机制实现了对属性变化的响应，即当某个值更新时，相关的监听器会自动被告知。

总结来说，`Delegates.observable()`提供了一种优雅的方式来处理属性的变更通知，使得管理多个依赖于某一数据源的对象变得更加高效和清晰。这样的设计提高了代码的可维护性和可读性。

```kotlin
class Person {
	var address: String by Delegates.observable("not entered yet!") {
		property, oldValue, newValue ->
		// update all existing shipments 
	}
}
```

反编译 Person 类，我们看到 Kotlin 编译器生成了一个扩展了 ObservableProperty 的类。

```kotlin
protected void afterChange(@NotNull KProperty property, Object oldValue, Object newValue) {
	// update all existing shipments
}
```

因此，可以看到在 `Delegates.observable` 的 `property` 为 `KProperty` .

`afterChange()` 函数由父类 `ObservableProperty` 的 `setter` 调用。这意味着每当调用者为 address 设置一个新值时，`setter` 将自动调用 `afterChange()` 函数，从而使所有监听器都被通知到此变化。

```kotlin
public override fun setValue(thisRef: Any?, property: KProperty<*>, value: T) {
	   val oldValue = this.value
	   if (!beforeChange(property, oldValue, value)) {
	       return
	   }
	   this.value = value
	   afterChange(property, oldValue, value)
}
```

### vetoable

 (vetoable) 是 Kotlin 提供的一个内置委托，允许开发者在属性值被修改之前进行干预。换句话说，它在修改过程中提供了某种控制机制，允许开发者根据某些条件决定是否允许该修改。

 **与 (observable) 委托的比较**：
   - (observable) 委托也是用于监听属性变化的机制，但它允许属性值的修改，(vetoable) 则可以拒绝这个修改。两者都可以回调一个处理程序来响应属性变更，但 (vetoable) 的设计目的是为了增加一种额外保护层，确保某些逻辑可以在值被变更之前执行。

 **参数**：
   - 初始值：这是属性初始状态的设置，指明该属性在开始时应有的值。
   - 监听器处理程序：当有操作企图修改这个属性的值时，这个处理程序会被调用。因此，开发者可以在这里添加逻辑，以决定是否继续执行修改操作。

```kotlin
var address: String by Delegates.vetoable("") {  property, oldValue, newValue ->
	newValue.length > 14
}
```

如果lambda条件返回true，则属性值将被修改，否则值将保持不变。在这种情况下，如果调用者尝试用小于15个字符的任何内容更新地址，则当前值将被保留。

查看反编译的`Person`类，Kotlin生成一个扩展了`ObservableProperty`的新类。生成的类包含我们在`beforeChange()`函数中传递的lambda，该lambda将在设置器设置值之前被调用。

```kotlin
public final class Person$$special$$inlined$vetoable$1 extends ObservableProperty {

  protected boolean beforeChange(@NotNull KProperty property, Object oldValue, Object newValue) {
     Intrinsics.checkParameterIsNotNull(property, "property");
     String newValue = (String)newValue;
     String var10001 = (String)oldValue;
     int var7 = false;
     return newValue.length() > 14;
  }
}
```

(vetoable) 委托为 Kotlin 开发者提供了一种灵活的方式来管理属性的可变性。它允许在属性值修改之前进行决策，这在处理复杂逻辑或需要保证一致性的场景中是十分有用的。通过这一机制，Kotlin 赋予了开发者对对象数据的更大控制能力，提高了代码的安全性和可维护性。

### notNull

Kotlin 标准库提供的最后一个内置委托是 `Delegates.notNull()`。

`notNull()` 允许属性在**稍后的时间**初始化， 类似 `lateinit`。在大多数情况下，推荐使用 `lateinit`，因为 `notNull()` 为每个属性创建了一个额外的对象。

```kotlin
val fullname : String  by  Delegates.notNull<String>()
```

反编译代码后:
**this**.**fullname$delegate** = Delegates.**_INSTANCE_**.notNull();

这个 `notNull()` 返回一个 `NotNullVar` 对象：

```kotlin
public fun  <T : Any> notNull(): ReadWriteProperty<Any?, T> = NotNullVar()
```

 **NotNullVar** 类是一种用于处理不可为空（non-nullable）变量的实现。它的主要功能是保存一个泛型的可空内部引用。这意味着这个引用可以是任意类型，但最初可能是空的（null）。

 **初始化检查**：在这个类中，重要的机制是它会抛出 `IllegalStateException`，如果任何代码在值被初始化之前调用了获取器（getter）。这意味着，在试图访问该引用的值之前，必须确保该值已经被正确地初始化。这样的设计能够有效地防止因使用未初始化值而引起的运行时错误。

```kotlin
private class NotNullVar<T : Any>() : ReadWriteProperty<Any?, T> {
	   private var value: T? = null
	
	   public override fun getValue(thisRef: Any?, property: KProperty<*>): T {
	       return value ?: throw IllegalStateException("Property ${property.name} should be initialized before get.")
	   }
	
	   public override fun setValue(thisRef: Any?, property: KProperty<*>, value: T) {
	       this.value = value
	   }
}
```

[**Built-in Delegates**](https://medium.com/androiddevelopers/built-in-delegates-4811947e781f)

---

## KProperty

### 1. `KProperty` 的定义

在Kotlin中，KProperty是反射API中的一个接口，用于表示类的**属性（property）**, 例如使用 `val` 或 `var` 声明的属性。

它允许你在运行时以类型安全的方式访问和操作属性，包括获取属性的**元数据**（如名称、类型）以及**读取**或**设置**属性的值。

`KProperty` 是Kotlin**反射机制**的重要组成部分，位于 `kotlin.reflect` 包中，广泛用于需要**动态**处理属性的场景。

###  2. 主要特点和作用

- **属性引用**：通过 `::` 操作符可以获取属性的引用。例如，对于一个类中的属性name，可以用 `ClassName::name` 获取它的 `KProperty` 对象。

- **访问属性值**：KProperty提供了`get`方法来读取属性的值。如果属性是可变的（用`var`定义），还可以通过`set`方法修改其值。

- **元数据访问**：通过KProperty，你可以获取属性的名称（name）、返回类型等信息。

- **接收者支持**：KProperty有多个子接口，根据属性的接收者（`receiver`，即属性的所有者对象）数量不同，分为：
    - `KProperty0`：无接收者，通常用于顶层属性或局部属性。
    - `KProperty1`：一个接收者，通常用于类中的成员属性。
    - `KProperty2`：两个接收者，通常用于扩展属性。

- **属性委托：**
    - 在 Kotlin 的属性委托机制中，`KProperty` 用于向委托对象提供有关属性的信息。
    - 当您使用属性委托时，委托对象可以访问 `KProperty` 实例，从而了解有关被委托属性的信息。

### 3. 使用示例

以下是一个简单的例子，展示如何使用KProperty：

```kotlin
class Person(val name: String)

fun main() {
    val person = Person("Alice")
    val property = Person::name  // 获取name属性的引用，返回KProperty1<Person, String>
    println(property.name)       // 输出属性的名称："name"
    println(property.get(person)) // 输出属性的值："Alice"
}
```

在这个例子中：

- `Person::name` 返回一个`KProperty1<Person, String>`对象，表示Person类中的name属性。
- 通过`property.name`可以获取**属性名称**。
- 通过`property.get(person)`可以获取 `person` 对象的 `name` **属性的值**。

### 4. 使用场景

- **序列化和反序列化：**
    - `KProperty` 可用于编写通用的序列化和反序列化代码，可以动态地处理不同对象的属性。
- **数据绑定：**
    - 在数据绑定框架中，`KProperty` 可用于观察属性的变化并更新 UI。
- **反射库：**
    - 当您需要编写使用反射的库时，`KProperty` 是一个重要的工具。
