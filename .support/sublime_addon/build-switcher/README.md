# BuildSwitcher (Sublime Text 2 plugin)

Do you have multiple build systems per project ? This plugin will help you quickly execute the one you want.

## Instalation
Recommended way is using [PackageControll] package.

Or you can download the [tarball] and extract it to your `~/Library/Application Support/Sublime Text 2/Packages/BuildSwitcher`.

## Configuration
There is currently no way to get list of available build systems in [Sublime], so you need to explicitly specify the ones you wanna list. Just add into your `XXX.sublime-project` something like this:

````
{
    "settings": {
        "build_switcher_systems": [
            "Unit tests",
            "CoffeeScript",
            ["My unit tests", "c:\\builds\\UI_tests.sublime-build"],
            ["My CoffeeScript", "/Users/me/build/coffee.sublime-build"]
        ]
    }
}
````

You can provide either build name only or custom name and build file path.

If you don't specify any build system, BuildSwitcher will just execute the currently selected build (the same behavior as Sublime's default `super+b` shortcut).

If you specify only one build system, it will execute it without asking.

If you specify multiple systems, you always get a pop up with options (sorted by usage).


Build variants can be specified by separating them from the build name using a pound sign “#.

So configuring:

"build_switcher_systems": ["Make", "Make#Install", ["MyMake#Install", "/Users/me/make.sublime-build"]]

and then choosing “Make#Install” will trigger the Make build system in the “Install” variant.

## Defining key shortcut
By default, "build_switcher" is mapped to `CMD+B`, however you can easily change that, just add to your keymap preferences:

````
{ "keys": ["super+b"], "command": "build_switcher" }
````



[Sublime]: http://www.sublimetext.com/
[PackageControll]: http://wbond.net/sublime_packages/package_control/installation
[tarball]: https://github.com/vojtajina/sublime-BuildSwitcher/tarball/master
