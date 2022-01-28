# AdaptiveBreakTimer



This is a kivy app designed to beat procrastination made primarily for people whose work (or study) time is flexible, like students. It tracks how much free time the user has. The timer goes up when the user is working at the modifiable rate of FreeTime / Work seconds per second, except when the user is sleeping. The only constraint it imposes on the user is that the timer must never be allowed to reach zero. The point is that this makes it easier to start studying, since work is immediately rewarded on the screen, and incentivizes
more fulfilling use of free time because being able to see your free time tick down makes you less likely to spend it on mindless scrolling. I and multiple friends of mine have had great results with it, so I'm going to clean up the graphics and publish it on the Play Store.

"Work/time:" accepts a string of a fraction that gets eval'd py python. It represents work time divided by total time spent not sleeping. If you work 9 hours/day excluding weekends, you type in "45/112".

The "Set timer:" text box accepts one, two or three numbers separated by a space or another reasonable character of choice. One number represents hours, two represent hours and minutes, and three represent days, hours and minutes.

"Sleep until:" accepts [hours] or [hours] [minutes] and uses system time.


Disclaimer: this was not made by a professional. It features lots of spaghetti, redundant code, confusing names, code that does nothing, global variables, and other things that professional developers might call "bad practice". I don't intend to update or maintain it once it's finished.
