from base64 import b64encode
from pathlib import Path

from anki import hooks
from anki.template import TemplateRenderContext, TemplateRenderOutput
from aqt import mw
from aqt.utils import *

from .extract_steps import extractSteps, getPositionsOf

delim = '!steps'
wrapperClsname = 'stepImagesWrapper'
ctrlRowClsname = 'stepImagesCtrlRow'
counterClsname = 'stepImagesCounter'
prevBtnClsname = 'stepImagesPrevBtn'
nextBtnClsname = 'stepImagesNextBtn'
inputClsname = 'stepImagesInput'
imgClsname = 'stepImagesImg'
descClsname = 'stepImagesDescription'
urlsAttr = 'urls'
descriptionsAttr = 'descriptions'
posAttr = 'pos'
cardAreaJsFile = os.path.join(Path(__file__).parent.absolute(), 'cardarea.js')

cssToInject = f'''
.{wrapperClsname} {{
    padding: .5rem;
}}

.{ctrlRowClsname} {{
    margin: .5rem;
}}

.{ctrlRowClsname} > * {{
    min-height: 1.5rem;
    font-size: 1rem;
    margin: 0 .5rem;
}}

.{inputClsname} {{
    width: 2rem;
    padding: 0 .5rem;
    background-color: #aaaaaa;
}}

.{descClsname} {{
    font-size: 1rem;
    opacity: 0.82;
}}
'''

with open(cardAreaJsFile, 'r') as fp:
    jsToInject = f'<script>{fp.read()}</script>'


def addonDisabled() -> bool:
    ankiDevEnv = os.environ.get('ANKI_DEV')
    dirpath = Path(__file__).parent.absolute()
    dirname = os.path.basename(os.path.normpath(dirpath))
    productionAddon = str(dirname)[0].isdigit()
    return (productionAddon and ankiDevEnv) or \
           (not productionAddon and not ankiDevEnv)


def refocusInterface():
    mw.web.setFocus()


def onCardDidRender(
        output: TemplateRenderOutput,
        context: TemplateRenderContext):
    output.question_text = alterText(output.question_text)
    output.answer_text = alterText(output.answer_text)
    output.css = cssToInject + output.css + os.linesep


def alterText(text: str) -> str:
    delimLen = len(delim)
    delimPositions = getPositionsOf(delim, text)
    out = ''

    if len(delimPositions) < 2:
        return text
    elif len(delimPositions) % 2 > 0:
        delimPositions.pop()

    for i in range(0, len(delimPositions), 2):
        lastDelimPos = -delimLen if i == 0 else delimPositions[i - 1]
        out += text[lastDelimPos + delimLen: delimPositions[i]]
        html = extractHTML(
            text[delimPositions[i] + delimLen: delimPositions[i + 1]])
        out += html

    return '{0}{1}\n{2}' \
        .format(out, text[delimPositions[-1] + delimLen:], jsToInject)


def extractHTML(text: str) -> str:
    steps = extractSteps(text)
    urls = ';'.join([i.imgurl for i in steps])
    descs = ';'.join([
        b64encode(str.encode(i.desc or '')).decode('utf-8') for i in steps])

    if len(steps) == 0:
        return text

    s1 = steps[0]

    return f'''
    <div class="{wrapperClsname}">
        <div class="{ctrlRowClsname}">
            <span class="{counterClsname}">1 / {len(steps)}</span>
            <button onclick="gg.onPrevClick(event)" 
                    class="{prevBtnClsname}">prev</button>
            <button onclick="gg.onNextClick(event)" 
                    class="{nextBtnClsname}">next</button>
            <input onkeyup="gg.onKeyup(event)" type="text" placeholder="[ or ]"
                    maxlength="0" class="{inputClsname}"/>
        </div>
        <img {posAttr}="0" src="{s1.imgurl}" {urlsAttr}="{urls}" 
                {descriptionsAttr}="{descs}" class="{imgClsname}">
        <p class="{descClsname}">{s1.desc or ''}</p>
    </div>
    '''


if not addonDisabled():
    hooks.card_did_render.append(onCardDidRender)

    # when u flip a card, the web ui loses focus so [] keyup's dont register
    # unless u click on the card area and focus it. this solves that problem.
    # src git/glutanimate/anki-addons-misc/blob/master/src/reviewer_refocus_card
    hooks.addHook("showQuestion", refocusInterface)
    hooks.addHook("showAnswer", refocusInterface)
