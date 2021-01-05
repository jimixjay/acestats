function drawScatter(title, x, y, texts, xrange, yrange, config) {
          trace1 = {
            type: 'scatter',
            x: x,
            y: y,
            mode: 'lines',
            name: 'Red',
            hovertext: texts,
            hoverinfo: 'text',
            fill: config.fill,
            hoverlabel: {
              bgcolor: '#fff',
              bordercolor: '#000'
            },
            line: {
              color: 'rgb(219, 64, 82)',
              width: 3
            }
          };

          var layout = {
              title: {
                text: title,
                size: 10
              },
              margin: {
                l: 50,
                r: 10,
                t: 50,
                b: 50
              },
              showlegend: config.showlegend,
              xaxis: {
                range: xrange
              },
              yaxis: {
                range: yrange,
                ticksuffix: config.suffix
              },
          };

          var data = [trace1];

          Plotly.newPlot(config.divId, data, layout, {responsive: true, scrollZoom: true});
        }

        function drawScatterPerSurface(title, trace1Data, trace2Data, trace3Data, trace4Data, xrange, yrange, config) {
            trace1 = {
              type: 'scatter',
              x: trace1Data.x,
              y: trace1Data.y,
              mode: 'lines',
              name: trace1Data.name,
              hovertext: trace1Data.texts,
              hoverinfo: 'text',
              fill: config.fill,
              hoverlabel: {
                bgcolor: '#fff',
                bordercolor: '#000'
              },
              line: {
                color: trace1Data.color,
                width: 2
              }
            };

            trace2 = {
              type: 'scatter',
              x: trace2Data.x,
              y: trace2Data.y,
              mode: 'lines',
              name: trace2Data.name,
              hovertext: trace2Data.texts,
              hoverinfo: 'text',
              /*fill: config.fill,*/
              /*hoverlabel: {
                bgcolor: '#fff',
                bordercolor: '#000'
              },*/
              line: {
                color: trace2Data.color,
                width: 2
              }
            };

            trace3 = {
              type: 'scatter',
              x: trace3Data.x,
              y: trace3Data.y,
              mode: 'lines',
              name: trace3Data.name,
              hovertext: trace3Data.texts,
              hoverinfo: 'text',
              /*fill: config.fill,*/
              /*hoverlabel: {
                bgcolor: '#fff',
                bordercolor: '#000'
              },*/
              line: {
                color: trace3Data.color,
                width: 2
              }
            };

            trace4 = {
              type: 'scatter',
              x: trace4Data.x,
              y: trace4Data.y,
              mode: 'lines',
              name: trace4Data.name,
              hovertext: trace4Data.texts,
              hoverinfo: 'text',
              /*fill: config.fill,*/
              /*hoverlabel: {
                bgcolor: '#fff',
                bordercolor: '#000'
              },*/
              line: {
                color: trace4Data.color,
                width: 2
              }
            };

            var layout = {
                title: {
                  text: title,
                  size: 10
                },
                margin: {
                  l: 50,
                  r: 10,
                  t: 50,
                  b: 50
                },
                showlegend: config.showlegend,
                xaxis: {
                  range: xrange
                },
                yaxis: {
                  range: yrange,
                 // ticksuffix: config.suffix
                },
            };

            var data = [trace1, trace2, trace3, trace4];

            Plotly.newPlot(config.divId, data, layout, {responsive: true, scrollZoom: true});
          }

        function drawBarChar(title, trace1Data, trace2Data, trace3Data, trace4Data, xrange, yrange, config) {
          trace1 = {
            type: 'bar',
            x: trace1Data.x,
            y: trace1Data.y,
            name: trace1Data.name,
            orientation: 'h',
            hovertext: trace1Data.texts,
            hoverinfo: 'text',
            hoverlabel: {
              bgcolor: '#fff',
              bordercolor: '#000'
            },
            marker: {
              color: trace1Data.color,
              width: 3
            }
          };

          trace2 = {
            type: 'bar',
            x: trace2Data.x,
            y: trace2Data.y,
            name: trace2Data.name,
            orientation: 'h',
            hovertext: trace2Data.texts,
            hoverinfo: 'text',
            hoverlabel: {
              bgcolor: '#fff',
              bordercolor: '#000'
            },
            marker: {
              color: trace2Data.color,
              width: 3
            }
          };

          trace3 = {
            type: 'bar',
            x: trace3Data.x,
            y: trace3Data.y,
            name: trace3Data.name,
            orientation: 'h',
            hovertext: trace3Data.texts,
            hoverinfo: 'text',
            hoverlabel: {
              bgcolor: '#fff',
              bordercolor: '#000'
            },
            marker: {
              color: trace3Data.color,
              width: 3
            }
          };

          trace4 = {
            type: 'bar',
            x: trace4Data.x,
            y: trace4Data.y,
            name: trace4Data.name,
            orientation: 'h',
            hovertext: trace4Data.texts,
            hoverinfo: 'text',
            hoverlabel: {
              bgcolor: '#fff',
              bordercolor: '#000'
            },
            marker: {
              color: trace4Data.color,
              width: 3
            }
          };

          var data = [trace1, trace2, trace3, trace4];

          var layout = {
              title: {
                text: title,
                size: 10
              },
              barmode: 'stack',
              /*margin: {
                l: 20,
                r: 10,
                t: 50,
                b: 50
              },*/
              showlegend: config.showlegend,
              /*xaxis: {
                range: xrange
              },
              yaxis: {
                range: yrange,
                ticksuffix: config.suffix
              },*/
          };

          Plotly.newPlot(config.divId, data, layout, {displayModeBar: false, responsive: true, scrollZoom: true});
        }