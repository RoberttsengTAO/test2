<template>
  <v-chart
    autoresize
    :option="echartOptions_sales"
    style="height: 50vh; border-radius: 4em"
  />
</template>

<script setup lang="ts">
import { defineProps, computed } from "vue";
import VChart from "vue-echarts";

// 接收來自父組件的資料
const props = defineProps({
  priceSalesData: Object,
});

// 計算圖表配置項
const echartOptions_sales = computed(() => ({
  backgroundColor: "#ffffff",
  textStyle: {
    color: "#592C63",
  },
  dataZoom: [
    {
      show: true,
      type: "slider",
      yAxisIndex: 0,
    },
  ],
  title: {
    text: "Sales",
    left: "left",
    textStyle: {
      color: "#592C63",
      fontSize: 36,
    },
    padding: [30, 30],
  },
  tooltip: {
    trigger: "item",
  },
  xAxis: {
    type: "category",
    data: ["Before", "After"],
  },
  yAxis: {
    type: "value",
    max:
      Math.max(
        props.priceSalesData.current_sales,
        props.priceSalesData.new_sales
      ) * 1.2,
    splitLine: {
      show: false,
    },
    position: "right",
  },

  series: [
    {
      name: "Sales",
      type: "bar",
      barWidth: "30%",
      data: [
        {
          value: props.priceSalesData.current_sales,
          itemStyle: { color: "#503291", borderRadius: [30, 0, 30, 0] },
        },

        {
          value: props.priceSalesData.new_sales,
          itemStyle: { color: "#2dbecd", borderRadius: [30, 0, 30, 0] },
        },
      ],

      markLine: {
        emphasis: {
          disable: false,
          label: {
            show: true,
          },
        },

        data: [
          [
            {
              x: 120,
              coord: ["Before", props.priceSalesData.current_sales],
              lineStyle: {
                color: "#eb3c96",
              },
              symbol: "arrow",
              symbolSize: 8,
              label: {
                position: "middle",
                rotate: 0,
                formatter: () => {
                  return `${
                    Math.round(
                      (10000 *
                        (props.priceSalesData.new_sales -
                          props.priceSalesData.current_sales)) /
                        props.priceSalesData.current_sales
                    ) / 100
                  } %`;
                },
              },
            },
            {
              x: 120,
              coord: ["Before", props.priceSalesData.new_sales],
              symbol: "arrow",
              symbolSize: 8,
            },
          ],
          [
            {
              tooltip: { formatter: "Current Sales: {c}" },
              value: props.priceSalesData.current_sales,
              x: 80,
              coord: [0, props.priceSalesData.current_sales],
              lineStyle: {
                color: "purple",
              },
              label: {
                position: "start",
                formatter: "Current Sales",
              },
            },
            {
              coord: ["Before", props.priceSalesData.current_sales],
              symbol: "none",
            },
          ],
          [
            {
              tooltip: { formatter: "New Sales: {c}" },
              value: props.priceSalesData.new_sales,
              x: 80,
              coord: [0, props.priceSalesData.new_sales],
              lineStyle: {
                color: "blue",
              },
              label: {
                position: "start",
                formatter: "New Sales",
              },
            },
            {
              coord: ["After", props.priceSalesData.new_sales],
              symbol: "none",
            },
          ],
        ],
      },
    },
  ],
}));
</script>
