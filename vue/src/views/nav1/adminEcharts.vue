<template>
    <section class="chart-container">
        <el-row>
            <el-col :span="12">
                <div id="chartPie1" style="width:100%; height:400px;"></div>
            </el-col>
            <el-col :span="12">
                <div id="chartPie2" style="width:100%; height:400px;"></div>
            </el-col>
        </el-row>
        <el-row>
            <el-col :span="24">
                <div id="chartPie3" style="width:100%; height:400px;"></div>
            </el-col>
        </el-row>
    </section>
</template>

<script>
import echarts from "echarts";
import { adminDrawPieChart } from "../../api/api";
export default {
  data() {
    return {
      chartPie1: null,
      chartPie2: null,
      chartPie3: null
    };
  },

  methods: {
    drawPieChart() {
      this.chartPie1 = echarts.init(document.getElementById("chartPie1"));
      this.chartPie2 = echarts.init(document.getElementById("chartPie2"));
      this.chartPie3 = echarts.init(document.getElementById("chartPie3"));
      let para = {user_id:this.$route.params.id}
      adminDrawPieChart(para).then(res => {
      console.log(res)
      let { code, value} = res.data
      //console.log(value.level1)
      if(code !== 200){
        this.$message({
          message:'服务器发生错误',
          type:'warning'
        })
      }else{
      let level1 = value.level1
      let level2 = value.level2
      let level3 = value.level3
      let data1 = Object.keys(level1)
      let data2 = Object.keys(level2)
      let data3 = Object.keys(level3)
      let len1 = data1.length
      let len2 = data2.length
      let len3 = data3.length
      let s1 = []
      let s2 = []
      let s3 = []
      for (var i = 0;i < len1; i++){
        var msg = {}
        msg.value = level1[data1[i]]
        msg.name = data1[i]
        s1.push(msg)
      }
      console.log(s1)
      for (var j = 0;j < len2; j++){
        var msg = {}
        msg.value = level2[data2[j]]
        msg.name = data2[j]
        s2.push(msg)
      }
      for (var k = 0;k < len3; k++){
        var msg = {}
        msg.value = level3[data3[k]]
        msg.name = data3[k]
        s3.push(msg)
      }
      let option1 = {
        title: {
          text: "一级研究方向",
          subtext: "总数:" + value['level1_total'],
          x: "center"
        },
        tooltip: {
          trigger: "item",
          formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        legend: {
          orient: "vertical",
          left: "left",
          data: data1
        },
        toolbox: {
          show: true,
          feature: {
            saveAsImage: {show: true}
          }
        },
        series: [
          {
            name: "占比数",
            type: "pie",
            radius: "55%",
            center: ["50%", "60%"],
            data: s1,
            itemStyle: {
              emphasis: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: "rgba(0, 0, 0, 0.5)"
              }
            }
          }
        ]
      };
      let option2 = {
        title: {
          text: "二级研究方向",
          subtext: "总数:" + value['level2_total'],
          x: "center"
        },
        tooltip: {
          trigger: "item",
          formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        legend: {
          orient: "vertical",
          left: "left",
          data: data2
        },
        toolbox: {
          show: true,
          feature: {
            saveAsImage: {show: true}
          }
        },
        series: [
          {
            name: "占比数",
            type: "pie",
            radius: "55%",
            center: ["50%", "60%"],
            data: s2,
            itemStyle: {
              emphasis: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: "rgba(0, 0, 0, 0.5)"
              }
            }
          }
        ]
      };
      let option3 = {
        title: {
          text: "三级研究方向",
          subtext: "总数:" + value['level3_total'],
          x: "center"
        },
        tooltip: {
          trigger: "item",
          formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        legend: {
          orient: "vertical",
          left: "left",
          data: data3
        },
        toolbox: {
          show: true,
          feature: {
            saveAsImage: {show: true}
          }
        },
        series: [
          {
            name: "占比数",
            type: "pie",
            radius: "55%",
            center: ["50%", "60%"],
            data: s3,
            itemStyle: {
              emphasis: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: "rgba(0, 0, 0, 0.5)"
              }
            }
          }
        ]
      };
      this.chartPie1.setOption(option1)
      this.chartPie2.setOption(option2)
      this.chartPie3.setOption(option3)
    }
    })
    },
    drawCharts() {
      this.drawPieChart();
    }
  },
  mounted: function() {
    this.drawCharts();
  },
  updated: function() {
    this.drawCharts();
  }
};
</script>

<style scoped>
.chart-container {
  width: 100%;
  float: left;
}
/*.chart div {
        height: 400px;
        float: left;
    }*/

.el-col {
  padding: 30px 20px;
}
</style>
