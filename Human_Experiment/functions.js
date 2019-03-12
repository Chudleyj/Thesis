
const prices =
       [54.63,
        99.15,
        95,
        74.38,
        82.2,
        107.23,
        71.95,
        80.8,
        98.17,
        95.52,
        120.51,
        151.08,
        157.2,
        200.7,
        300,
        248.48,
        164.58,
        77.9,
        59.93,
        99.9,
        104.04,
        144.13,
        179.9,
        120.85,
        154.76,
        150.24,
        131.13,
        110.96,
        119.4,
        135.89,
        152.32,
        192.91,
        177.2,
        181.16,
        177.3,
        200.13,
        235.41,
        269.23,
        291.9,
        280.9,
        404.39,
        488.4,
        499.47,
        435.69,
        583.65,
        679.36,
        615.89,
        731.14,
        652.1,
        762.95,
        874.13,
        969.26,
        785.69,
        905.11,
        943.75,
        800.36,
        838.92,
        890.2,
        1020.02,
        850.86,
        616.24,
        852.41,
        1004.65,
        831.17,
        805.01,
        838.74,
        963.99,
        875,
        1046.54,
        1258.64,
        1211.57,
        1546.67,
        1895.95,
        1938.83,
        2168.57,
        2753.2,
        2633.66,
        3168.83,
        3301.11,
        3754.09,
        3834.44,
        5117.12,
        6448.27,
        7908.3,
        9181.43,
        11497.12,
        10787.99,
        10021.57,
        8341.63,
        10453.92,
        10783.01,
        10717.5,
        12463.15,
        13264.82,
        8776.39,
        10428.05,
        11577.51,
        12217.56,
        13104.14,
        16576.66,
        17823.07,
        17425.03,
        19762.6,
        24719.22]

const dates =
       ['12/31/1914',
        '12/31/1915',
        '12/30/1916',
        '12/31/1917',
        '12/31/1918',
        '12/31/1919',
        '12/31/1920',
        '12/31/1921',
        '12/30/1922',
        '12/31/1923',
        '12/31/1924',
        '12/31/1925',
        '12/31/1926',
        '12/31/1927',
        '12/31/1928',
        '12/31/1929',
        '12/31/1930',
        '12/31/1931',
        '12/31/1932',
        '12/30/1933',
        '12/31/1934',
        '12/31/1935',
        '12/31/1936',
        '12/31/1937',
        '12/31/1938',
        '12/30/1939',
        '12/31/1940',
        '12/31/1941',
        '12/31/1942',
        '12/31/1943',
        '12/30/1944',
        '12/31/1945',
        '12/31/1946',
        '12/31/1947',
        '12/31/1948',
        '12/31/1949',
        '12/30/1950',
        '12/31/1951',
        '12/31/1952',
        '12/31/1953',
        '12/31/1954',
        '12/30/1955',
        '12/31/1956',
        '12/31/1957',
        '12/31/1958',
        '12/31/1959',
        '12/30/1960',
        '12/29/1961',
        '12/31/1962',
        '12/31/1963',
        '12/31/1964',
        '12/31/1965',
        '12/30/1966',
        '12/29/1967',
        '12/31/1968',
        '12/31/1969',
        '12/31/1970',
        '12/31/1971',
        '12/29/1972',
        '12/31/1973',
        '12/31/1974',
        '12/31/1975',
        '12/31/1976',
        '12/30/1977',
        '12/29/1978',
        '12/31/1979',
        '12/31/1980',
        '12/31/1981',
        '12/31/1982',
        '12/30/1983',
        '12/31/1984',
        '12/31/1985',
        '12/31/1986',
        '12/31/1987',
        '12/30/1988',
        '12/29/1989',
        '12/31/1990',
        '12/31/1991',
        '12/31/1992',
        '12/31/1993',
        '12/30/1994',
        '12/29/1995',
        '12/31/1996',
        '12/31/1997',
        '12/31/1998',
        '12/31/1999',
        '12/29/2000',
        '12/31/2001',
        '12/31/2002',
        '12/31/2003',
        '12/31/2004',
        '12/30/2005',
        '12/29/2006',
        '12/31/2007',
        '12/31/2008',
        '12/31/2009',
        '12/31/2010',
        '12/30/2011',
        '12/31/2012',
        '12/31/2013',
        '12/31/2014',
        '12/31/2015',
        '12/30/2016',
        '12/29/2017']

let bal = 10000
let balance = 10000

let sharesOwned = 5

let currTrial = 0

let shareBought = false

let balanceChange = 0

let balanceChangeStr = "null"

/*
  let choice keep tracks of which combination of buy, sell, and hold options
  are legal for a user during a certian trial
*/
let choice = 3

document.addEventListener('DOMContentLoaded', function ()
{
  const nTrials = prices.length-1

  fullscreen = {type: 'fullscreen', fullscreen_mode: true}

  timeline = []

  timeline.push(fullscreen)
  timeline.push(welcomeScreen)
  timeline.push(insctructionsScreen)
  timeline.push(accInfoIntroScreen)
  timeline.push(priceDateScreen)
  timeline.push(buySellHoldScreen)

  for(let i = currTrial; i < nTrials; i++)
  {
    timeline.push(accInfoScreen)
    timeline.push(priceDateScreen)
    timeline.push(buySellHoldScreen)
  }

  jsPsych.init({
      timeline: timeline,
      on_finish: function(data){jsPsych.data.get().localSave('csv', `data.csv`)}
  })

});


/*
  Key press values:
   Space: 32
   F: 70
   J: 74
*/
function updateBalance()
{
  const trialData = jsPsych.data.getLastTrialData()

  //Hold
  if(trialData.values()[0].key_press == 32){
    return balance
  }

  //Buy
  else if(trialData.values()[0].key_press == 70){
    bal = bal - prices[trialData.values()[0].trial_number-1]
    balance = bal + (prices[trialData.values()[0].trial_number] * sharesOwned)
    balanceChange = prices[trialData.values()[0].trial_number] - prices[trialData.values()[0].trial_number-1]
    balanceChangeStr = balanceChange.toLocaleString()
    if(balanceChange > 0)
      balanceChangeStr = "+" + balanceChangeStr
    return balance
  }

  //Sell
  else if(trialData.values()[0].key_press == 74){
    bal = bal + prices[trialData.values()[0].trial_number-1]
    balance = bal + (prices[trialData.values()[0].trial_number] * sharesOwned)
    balanceChange = prices[trialData.values()[0].trial_number] - prices[trialData.values()[0].trial_number-1]
    balanceChangeStr = balanceChange.toLocaleString()
    if(balanceChange > 0)
      balanceChangeStr = "+" + balanceChangeStr
    return balance
  }

}

function updateShares()
{
  const trialData = jsPsych.data.getLastTrialData()

  //Hold
  if(trialData.values()[0].key_press == 32){
    return
  }

  //Buy
  else if(trialData.values()[0].key_press == 70){
    sharesOwned = sharesOwned + 1
    shareBought = true
  }

  //Sell
  else if(trialData.values()[0].key_press == 74){
    sharesOwned =  sharesOwned - 1
    shareBought = false
  }
}

let accInfoIntroScreen =
{
  type: 'html-keyboard-response',
  response_ends_trial: true,
  choices: jsPsych.NO_KEYS,
  trial_duration: 4000,
  stimulus: function()
  {
    return `<p>Account Balance: $${balance}</p>
            <p>Shares Owned: ${sharesOwned}</p>`;
  }
};

let accInfoScreen =
{
  type: 'html-keyboard-response',
  response_ends_trial: true,
  choices: jsPsych.NO_KEYS,
  trial_duration: 4000,
  stimulus: function()
  {
      if(shareBought){
        if(balanceChange > 0){
          return `<div id="ParentDiv">
                    <div id="Balance" style="float:left;">
                      <p>Total Assets: <strong>$${balance.toLocaleString()}</strong>
                      <font color = "#00cc00"> <strong> ${balanceChangeStr}</strong></font></p>
                    </div>
                    <br>
                    <div id = "Shares" style="float:left;">
                      <p>&emsp; Shares Owned: <strong>${sharesOwned}</strong>
                      <font color = "#00cc00"><strong>+1</strong></font></p>
                    </div>
                  </div>`;
        }
        else{
          return `<div id="ParentDiv">
                    <div id="Balance" style="float:left;">
                      <p>Total Assets: <strong>$${balance.toLocaleString()}</strong>
                      <font color = "#ff0000"> <strong> ${balanceChangeStr}</strong></font></p>
                    </div>
                    <br>
                    <div id = "Shares" style="float:left;">
                      <p>&emsp; Shares Owned: <strong>${sharesOwned}</strong>
                      <font color = "#00cc00"><strong>+1</strong></font></p>
                    </div>
                  </div>`;
        }
      }
      else{
        if(balanceChange > 0){
          return `<div id="ParentDiv">
                    <div id="Balance" style="float:left;">
                      <p>Account Balance: <strong>$${balance.toLocaleString()}</strong>
                      <font color = "#00cc00"> <strong> ${balanceChangeStr}</strong></font></p>
                    </div>
                    <div id="Shares" style="float:left;">
                      <p>&emsp; Shares Owned: <strong>${sharesOwned}</strong>
                      <font color = "#ff0000">&emsp; <strong>-1</strong></font></p>
                    </div>
                  </div>`;
      }
        else{
          return `<div id="ParentDiv">
                    <div id="Balance" style="float:left;">
                      <p>Account Balance: <strong>$${balance.toLocaleString()}</strong>
                      <font color = "#ff0000"> <strong> ${balanceChangeStr}</strong></font></p>
                    </div>
                    <div id="Shares" style="float:left;">
                      <p>&emsp; Shares Owned: <strong>${sharesOwned}</strong>
                      <font color = "#ff0000">&emsp; <strong>-1</strong></font></p>
                    </div>
                  </div>`;
      }
    }
  }
};

let buySellHoldScreen =
{
  type: 'html-keyboard-response',
  response_ends_trial: true,
  choices: ["f", "j"],
  data: function(){return ({trial: 'buySellHold', trial_number: currTrial, date: dates[currTrial], price: prices[currTrial]})},
  stimulus: function()
  {
      return `<div id ="ParentDiv" style = "align-text:center; width:100%;">
                <p>Would you like to buy or sell a share for: $${prices[currTrial-1]}</p>
                <div id="Buy" style ="position: relative; display: inline-block;">
                  <p>Buy</p>
                  <p>( <strong>F</strong> )</p>
                </div>
                <div id="Sell" style ="position: relative; display: inline-block;">
                  <p>&emsp; Sell</p>
                  <p>&emsp; ( <strong>J</strong> )</p>
                </div>
              </div>`;
  },
  on_finish: function(trial_data)
  {
    updateShares()
    updateBalance()
    jsPsych.data.addDataToLastTrial
    ({
      choice: trial_data.key_press == jsPsych.pluginAPI.convertKeyCharacterToKeyCode('F') ? "buy" : "sell",
      balance: balance,
      shares: sharesOwned
    })
  }
};

let insctructionsScreen =
{
  type: 'html-keyboard-response',
  response_ends_trial: true,
  choices:["space"],
  stimulus: `<p class='very-large center-content'>During this experiment you will be buying and selling shares on a simulated stock market.</p>
             <p>You will start with $10,000 and 5 shares.</p>
             <p>You will be shown dates and the price of the stock on that date. You will then either buy or sell a share on that date.</p>
             <p>Place your left index finger on the 'F' key and your right index finger on the 'J' key and leave them there for the entire experiment.</p>
             <p>Press the 'Space Key' to begin.</p>`,
  timing_post_trial: 0
}

let priceDateScreen =
{
  type: 'html-keyboard-response',
  response_ends_trial: true,
  choices:["space"],
  stimulus: function()
    {
      currTrial++;
      return `<br><br><br><br><br><br><br><br>
              <p>Date: ${dates[currTrial-1]}</p>
              <p>Price: $${prices[currTrial-1]}</p>
              <br><br><br><br><br><br><br><br><br><br><br>
              <p style="display: table-row; vertical-align: bottom; text-align: center">Press <strong>Space</strong> to continue</p>`;
    }
}

let welcomeScreen =
{
    type: 'html-keyboard-response',
    stimulus: `<p class='very-large center-content'>Welcome.</p>
               <p class='center-content'>Wait until you are told to begin, then hit any key for the insctructions</p>`,
    response_ends_trial: true,
    timing_post_trial: 0
}
