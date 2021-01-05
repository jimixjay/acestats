function getWinsRating(url) {
  showLoader('canvas-winRating');
  Plotly.purge('canvas-winRating');
  $.ajax({
    'type': 'get',
    'url': url,
    'success': function(data) {
      console.log(data);
      //data = JSON.parse(data);
      var x = [];
      var y = [];
      var texts = [];
      var xrange = [];
      var loopIndex = 0;
      var lastYear = '';
      Object.entries(data).forEach(function(element, index, array) {
        if (loopIndex == 0) {
          xrange.push(element[0]);
        }
        loopIndex++;

        x.push(element[0]);
        y.push(element[1]['rating']);
        texts.push("Year: " + element[0] + "<br>Wins: " + element[1]['wins'] + "<br>Losses: " + element[1]['losses']);
        lastYear = element[0];
      });

      xrange.push(lastYear);

      drawScatter('Win rating by year', x, y, texts, xrange, [0, 100], {fill: 'tozeroy', suffix: "%", divId: "canvas-winRating", showlegend: false});
      showVisualization('canvas-winRating');
    }
  });
}

function getAcesPerGamePerSurface(url) {
    multipleLinesConstructor(url, 'aces', 'aces', 2);
}

function getDoubleFaultsPerGamePerSurface(url) {
    multipleLinesConstructor(url, 'doubleFaults', 'double faults', 1);
}

function getServicePointsPerGamePerSurface(url) {
    multipleLinesConstructor(url, 'servicePoints', 'service points', 5);
}

function multipleLinesConstructor(url, idField, field, extraMaxY) {
  showLoader('canvas-' + idField + 'PerGamePerSurface');
  Plotly.purge('canvas-' + idField + 'PerGamePerSurface');
  $.ajax({
    'type': 'get',
    'url': url,
    'success': function(data) {
      console.log(data);
      //data = JSON.parse(data);
      var trace1 = [];
      trace1['x'] = [];
      trace1['y'] = [];
      trace1['texts'] = [];
      trace1['color'] = '#7f91c7';
      trace1['name'] = 'Hard';

      var trace2 = [];
      trace2['x'] = [];
      trace2['y'] = [];
      trace2['texts'] = [];
      trace2['color'] = '#c9891a';
      trace2['name'] = 'Clay';

      var trace3 = [];
      trace3['x'] = [];
      trace3['y'] = [];
      trace3['texts'] = [];
      trace3['color'] = '#3c821b';
      trace3['name'] = 'Grass';

      var trace4 = [];
      trace4['x'] = [];
      trace4['y'] = [];
      trace4['texts'] = [];
      trace4['color'] = '#0a1678';
      trace4['name'] = 'Carpet';

      var xrange = [];
      var maxAces = 0;
      var loopIndex = 0;
      var lastYear = '';
      Object.entries(data).forEach(function(element, index, array) {
        if (loopIndex == 0) {
          xrange.push(element[0]);
        }
        loopIndex++;

        var averageAces = 0;
        var games = 0;

        trace1.x.push(element[0]);
        if ('Hard' in element[1]) {
          averageAces = element[1]['Hard'][idField] / element[1]['Hard']['games'];
          games = element[1]['Hard']['games'];

          if (averageAces > maxAces) {
            maxAces = averageAces;
          }
        } else {
          averageAces = 0;
          games = 0;
        }
        trace1.y.push(averageAces);
        if (games != 0 && averageAces != 0) {
          trace1.texts.push("<b>Hard</b> " + averageAces.toFixed(2) + " " + field + " per game<br>in " + games + " in games played");
        } else {
            trace1.texts.push("<b>Hard</b> 0 " + field + " per game");
        }

        trace2.x.push(element[0]);
        if ('Clay' in element[1]) {
          averageAces = element[1]['Clay'][idField] / element[1]['Clay']['games'];
          games = element[1]['Clay']['games'];

          if (averageAces > maxAces) {
            maxAces = averageAces;
          }
        } else {
          averageAces = 0;
          games = 0;
        }
        trace2.y.push(averageAces);
        if (games != 0 && averageAces != 0) {
          trace2.texts.push("<b>Clay</b> " + averageAces.toFixed(2) + " " + field + " per game<br>in " + games + " in games played");
        } else {
          trace2.texts.push("<b>Clay</b> 0 " + field + " per game");
        }

        trace3.x.push(element[0]);
        if ('Grass' in element[1]) {
          averageAces = element[1]['Grass'][idField] / element[1]['Grass']['games'];
          games = element[1]['Grass']['games'];

          if (averageAces > maxAces) {
            maxAces = averageAces;
          }

        } else {
          averageAces = 0;
          games = 0;
        }
        trace3.y.push(averageAces);
        if (games != 0 && averageAces != 0) {
          trace3.texts.push("<b>Grass</b> " + averageAces.toFixed(2) + " " + field + " per game<br>in " + games + " in games played");
        } else {
           trace3.texts.push("<b>Grass</b> 0 " + field + " per game");
        }

        trace4.x.push(element[0]);
        if ('Carpet' in element[1]) {
          averageAces = element[1]['Carpet'][idField] / element[1]['Carpet']['games'];
          games = element[1]['Carpet']['games'];

          if (averageAces > maxAces) {
            maxAces = averageAces;
          }
        } else {
          averageAces = 0;
          games = 0;
        }
        trace4.y.push(averageAces);
        if (games != 0 && averageAces != 0) {
          trace4.texts.push("<b>Carpet</b> " + averageAces.toFixed(2) + " " + field + " per game<br>in " + games + " in games played");
        } else {
            trace4.texts.push("<b>Carpet</b> 0 " + field + " per game");
        }

        lastYear = element[0];
      });

      xrange.push(lastYear);

      drawScatterPerSurface(field.charAt(0).toUpperCase() + field.slice(1) + ' per game', trace1, trace2, trace3, trace4, xrange, [0, maxAces + extraMaxY], {fill: 'none', suffix: " " + field, divId: "canvas-" + idField + "PerGamePerSurface", showlegend: true});
      showVisualization('canvas-' + idField + 'PerGamePerSurface');
    }
  });
}