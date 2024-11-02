// ==UserScript==
// @name        Custom Desmos Function
// @namespace   github.com/jared-hughes
// @match       *://www.desmos.com/calculator*
// @description Custom function in Desmos, including custom autoOperatorNames. Warning: currently incompatible with other scripts that manipulate the worker, such as desmos god mode.
// @grant       none
// @version     0.1.1
// @run-at      document-start
// @author      fireflame241 (Jared Hughes)
// ==/UserScript==

/* To change the function, ctrl+F for "getYearStart" and edit */


// the function definition itself

function getMonthEnd(month, year) {
    
    let mon31 = [12, 10, 8, 7, 5, 3, 1]
    let i = 0
    let out = 28
    while (i < mon31.length) {
        if (mon31[i] == month) {
            out = 31
        }
        i = i + 1
    }

    if (out != 31) {
        if (month != 2) {
            out = 30
        }
    }
    
    if ((month == 2) && ((year % 4) == 0)) {
        out = 29
    }
    
    return out
}

function getDayOfFourYear(dateArray) {
    let day = -1
    let month = 1
    while (month < dateArray[1]) {
        day = day + getMonthEnd(month, dateArray[0])
        month = month + 1
    }
    day = day + dateArray[2] + (dateArray[3] / 24) + (dateArray[4] / 24 / 60) + (dateArray[5] / 24 / 60 / 60)
    
    let yearf = Math.floor(dateArray[0] / 4) * 4
    while (yearf != dateArray[0]) {
        if ((yearf % 4) == 0) {
            day = day + 366
        } else {
            day = day + 365
        }
        yearf = yearf + 1
    }

    return day
}
    
function getYearDecimal(dateArray) {
    let day = -1
    let month = 1
    while (month < dateArray[1]) {
        day = day + getMonthEnd(month, dateArray[0])
        month = month + 1
    }
    day = day + dateArray[2] + (dateArray[3] / 24) + (dateArray[4] / 24 / 60) + (dateArray[5] / 24 / 60 / 60)
    if ((dateArray[0] % 4) == 0) {
        return dateArray[0] + (day / 366)
    } else {
        return dateArray[0] + (day / 365)
    }
}

function getYearStart(x) {

    let dateArray = [parseFloat(x), 1, 1, 0, 0, 0]

    let yearsSince0 = getYearDecimal(dateArray)
    
    let daysSince0 = (Math.floor(yearsSince0 / 4) * 1461) + getDayOfFourYear(dateArray) + 1
    
    return daysSince0 * 24 * 60 * 60
}

window.Worker = new Proxy(Worker, {
  construct(target, args) {
    if (args[0].startsWith("blob:")) {
      const xhr = new XMLHttpRequest
      xhr.open("GET", args[0], false)
      xhr.send()
      const hooked = xhr.responseText
        // Define BuiltIn.getYearStart to be the above function
        .replace(/Object.defineProperty\((?<exports>.),"sinh"/g, `
Object.defineProperty($<exports>, "getYearStart", {
  enumerable: true,
  get: function() {
    return ${getYearStart.toString()}
  }
}), $&`)
        // Mark getYearStart as a builtin that calls BuiltIn.getYearStart(x)
        .replace(/sinh:(?<func>.)\("BuiltIn","sinh"/, `getYearStart:$<func>("BuiltIn","getYearStart"), $&`)
      args[0] = URL.createObjectURL(new Blob([hooked]))
    }
    return new target(...args)
  }
})

function applyNames() {
  /* see https://github.com/jared-hughes/DesThree/blob/master/src/View.js#L66 for more info, including forcing a rerender */
  const fields = document.querySelectorAll('.dcg-mq-editable-field')
  fields.forEach(field => {
    const opt = field._mqMathFieldInstance.__controller.root.cursor.options;
    // allow getYearStart to be written without manipulating LaTeX in the console
    opt.autoOperatorNames.getYearStart = 'getYearStart'
  })
}


function initialRerender() {
  window.Calc.getExpressions()
    .filter(e => e.type === 'expression')
    .forEach(e => {
      const selector = `.dcg-expressionitem[expr-id='${e.id}'] .dcg-mq-editable-field`
      const mqField = document.querySelector(selector)
      console.log(selector)
      // mqField._mqMathFieldInstance.__controller.renderLatexMath(e.latex)
    })
}

function init() {
  window.Calc.controller.dispatcher.register(e => {
    if (
      ['tick', 'new-expression', 'new-expression-at-end'].includes(e.type) ||
      (e.type === 'on-special-key-pressed' && e.key === 'Enter')
    ) {
      // update the math field of new expression elements
      applyNames()
    }
  })
  applyNames()
  initialRerender()
}

const interval = setInterval(() => {
  if (window.Calc && window.Calc.controller) {
    clearInterval(interval)
    init()
  }
}, 50)