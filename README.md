# anki-step-images (Image Carousels)
This addon allows you to step through images that belong together. For example, if you want images A,B and C to be in a carousel, place the following somewhere in the field value text editor:
```
!steps
{imgA}
{imgB}
{imgC}
!steps
```

When Anki renders a card, it passes the generated HTML to this addon. This addon will then look for the above pattern and replace it with HTML/Javascript to make a carousel possible. You may step through the images in the carousel a few different ways. 

If there is more than one carousel in the rendered card:
- press the prev button or type `[` in the input box displayed for that carousel to go to the previous image in the carousel.
- press the next button or type `]` in the input box displayed for that carousel to go to the next image in the carousel.

Otherwise, if there is only one carousel in the rendered card, in addition to the above you may:
- type `[`,`]` anywhere to go to the previous/next image in the carousel, respectively.

You may add an optional description for any number of the images in the field value text editor like so:
```
!steps
{imgA}
!stepd this is a description for imgB !stepd
{imgB}
!stepd this is a description for imgC !stepd
{imgC}
!steps
```

Note the description must be placed above the image you want it for and below the previous image.

### styling 

You may override the default styling for different components of the carousel to your liking. The css classes you can override are:
```
stepImagesWrapper
stepImagesCtrlRow
stepImagesCounter
stepImagesPrevBtn
stepImagesNextBtn
stepImagesInput
stepImagesImg
stepImagesDescription
```

The following is the html structure used for the carousel. This may help if you do want to customize the style.

```
<div class="stepImagesWrapper">
    <div class="stepImagesCtrlRow">
        <span class="stepImagesCounter"></span>
        <button class="stepImagesPrevBtn">prev</button>
        <button class="stepImagesNextBtn">next</button>
        <input class="stepImagesInput"/>
    </div>
    <img class="stepImagesImg">
    <p class="stepImagesDescription"></p>
</div>
```

### example - tying a knot
Given the following (partial) entered into a field value text area:

![knot-demo](https://user-images.githubusercontent.com/25497140/97955827-00a5e180-1d5c-11eb-9aab-788bf09e0d68.jpg)

the following carousel will be generated:

![example carousel](https://user-images.githubusercontent.com/25497140/97954906-a277ff00-1d59-11eb-9b44-c40c2db8fc44.gif)

### developing
Make changes and then run `python build.py test`. This will work for Anki 2.1 on OSX. If you have a different OS you will need to modify `./build.py` accordingly. 

To generate `knot-demo.gif`, I used quicktime screen recording to create a .mov file and then converted it to gif via
```
ffmpeg -i knot-demo.mov -s 400x526 -r 10 knot-demo.gif
```

### deploying
```
python build.py dist
```
the .addon file you need to upload will be placed in `dist/`. for the description you enter @ https://ankiweb.net/shared/upload paste this README and edit accordingly.