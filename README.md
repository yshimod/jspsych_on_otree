# jspsych_on_otree

- To use [jsPsych](https://www.jspsych.org/7.2/) with [oTree](https://otree.readthedocs.io/en/latest/), you should add a `<div>` element outside the `{{ block content }}` (i.e., outside the `#form` element) and specify the `<div>` element as the `initJsPsych`'s `display_element` attribute.

- To submit data collected by jsPsych to the oTree server, in the `initJsPsych`'s `on_finish` function, you should add an `<input type="hidden">` element, with your data for the `value` attribute, to the `#form` element (using jQuery), and then you should submit the page (by calling `$('#form').submit()`).

- References:  
[https://kywch.github.io/jsPsych-in-Qualtrics/](https://kywch.github.io/jsPsych-in-Qualtrics/)
