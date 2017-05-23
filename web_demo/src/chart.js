export const drawChart = (dates, maxs, mins, avgs) => {

  var chart = echarts.init(document.getElementById('chart'));
  var option = {
      tooltip : {
          trigger: 'axis'
      },
      legend: {
          data:['平均', '最低', '最高']
      },
      grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
      },
      xAxis : [{
          type : 'category',
          data : dates
      }],
      yAxis : [{
          type : 'value',
          name : '万元/平米'
      }],
      series : [{
            name: '平均',
            type:'line',
            data: avgs
        },
        {
            name:'最低',
            type:'line',
            data: mins
        },
        {
            name:'最高',
            type:'line',
            data: maxs
        }
      ]
  };
  chart.setOption(option);
  var chartResize = () => {
    if ($(window).width() < 768) {
      $("#chart").css("width", ($(window).width() - 60) + "px")
    } else {
      $("#chart").css("width", ($(window).width() - 200) + "px")
    }
    chart.resize();
  }
  chartResize();
  window.onresize = chartResize;
}
