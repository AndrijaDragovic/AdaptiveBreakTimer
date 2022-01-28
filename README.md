# AdaptiveBreakTimer

This was made in two afternoons by someone who is learning programming. It features lots of spaghetti, redundant code, confusing names, code that does nothing, global variables, and other things that professional developers might call "bad practice". I don't intend to update or maintain it once it's finished.

The timer tracks how much free time the user has, made primarily for people whose work (or study) time is completely flexible, like some college students. The timer goes up when the user is working according to a fraction specified in the settings menu, except when the user is sleeping.

"Work/time:" accepts a string of a fraction that gets eval'd py python. It represents work time divided by total time spent not sleeping. If you work 9 hours/day excluding weekends, you type in "45/112".

The "Set timer:" text box accepts one, two or three numbers separated by a space or another reasonable character of choice. One number represents hours, two represent hours and minutes, and three represent days, hours and minutes.

"Sleep until:" accepts [hours] or [hours] [minutes] and uses system time.
