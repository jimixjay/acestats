function getRankings(url) {
          $.ajax({
            'type': 'get',
            'url': url,
            'success': function(data) {
              $("#rankings").html("")
              console.log(data);
              //data = JSON.parse(data);
              var x = [];
              var y = [];
              var texts = [];
              var xrange = [];
              var loopIndex = 0;
              var lastRange = '';
              var minRank = 501;
              var maxRank = 0;
              Object.entries(data).forEach(function(element, index, array) {
                if (loopIndex == 0) {
                  xrange.push(element[0]);
                }
                loopIndex++;

                if (element[1] > maxRank) {
                  maxRank = element[1]
                }

                if (element[1] < minRank) {
                  minRank = element[1]
                }

                x.push(element[0]);
                y.push(element[1]);
                texts.push(element[0] + " rank: " + element[1]);
                lastRange = element[0];
              });

              xrange.push(lastRange);

              var diffRank = maxRank - minRank;
              while (diffRank > 100) {
                maxRank = maxRank / 2;
                diffRank = maxRank - minRank
              }

              if (minRank < 10) {
                minRank = 10.5
              }

              drawScatter('Historic ATP ranking', x, y, texts, xrange, [maxRank + 10, minRank - 10], {fill: 'none', suffix: "", divId: "rankings", showlegend: false});
              showVisualization();
            }
          });
        }