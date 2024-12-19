<template>
  <v-chart
    autoresize
    :option="echartOptions_price"
    style="height: 50vh; border-radius: 4em"
  />
</template>

<script setup lang="ts">
import { defineProps, computed } from "vue";
import VChart from "vue-echarts";

const props = withDefaults(
  defineProps<{
    priceSalesData?: {
      current_sales: number;
      new_sales: number;
      current_price: number;
      new_price: number;
      highest_price: number;
      lowest_price: number;
      floor_price: number;
      NHIA_price: number;
    };
    updateClients?: Array<any>;
    checkedIndex?: number;
  }>(),
  {
    priceSalesData: () => ({
      current_sales: 0,
      new_sales: 0,
      current_price: 0,
      new_price: 0,
      highest_price: 0,
      lowest_price: 0,
      floor_price: 0,
      NHIA_price: 0,
    }),
    updateClients: () => [],
    checkedIndex: 0,
  }
);

const echartOptions_price = computed(() => ({
  backgroundColor: "#ffffff",
  textStyle: {
    color: "#592C63",
  },

  title: {
    text: "Price",
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
  dataZoom: [
    {
      minValueSpan: Math.min(
        props.priceSalesData.lowest_price,
        props.priceSalesData.floor_price,
        props.priceSalesData.NHIA_price,
        props.priceSalesData.new_price
      ),
      show: true,
      type: "slider",
      yAxisIndex: 0,
    },
  ],
  xAxis: {
    type: "category",
    offset: 10,
    data: ["Before", "After"],
  },
  grid: {
    left: "30%",
  },
  yAxis: {
    max: props.priceSalesData.highest_price * 1.1,
    type: "value",
    splitLine: {
      show: false,
    },
    position: "right",
  },
  toolip: {
    trigger: "item",
  },
  series: [
    {
      name: "",
      type: "bar",
      data: [
        {
          emphasis: { disable: true },
          value: props.priceSalesData.current_price.toFixed(2),
          itemStyle: { color: "#503291", borderRadius: [30, 0, 30, 0] },
        },

        {
          value: props.priceSalesData.new_price.toFixed(2),
          itemStyle: { color: "#2dbecd", borderRadius: [30, 0, 30, 0] },
        },
      ],
      barWidth: "30%",
      markPoint: {
        tooltip: {
          formatter: props.updateClients[props.checkedIndex].client + ": {c}",
        },
        data: [
          {
            name: "Before Price",
            value: props.updateClients[props.checkedIndex].currentAspPrice,
            xAxis: "Before",
            label: {
              show: false,
              backgroundColor: "transparent",
              formatter:
                props.updateClients[props.checkedIndex].client + ": {c}",
              position: "right",
            },
            yAxis: props.updateClients[props.checkedIndex].currentAspPrice,
          },
          {
            tooltip: {
              formatter:
                props.updateClients[props.checkedIndex].client + ": {c}",
            },
            name: "Negotiated Price",
            value: props.updateClients[props.checkedIndex].negotiatedPrice,
            xAxis: "After",
            label: {
              show: false,
              backgroundColor: "transparent",
              formatter:
                props.updateClients[props.checkedIndex].client + ": {c}",
              position: "right",
            },

            yAxis: props.updateClients[props.checkedIndex].negotiatedPrice,
          },
        ],

        itemStyle: {
          color: "rgba(230, 30, 80, 1)",
        },

        symbol: "circle",
        symbolSize: 15,
      },
      markLine: {
        tooltip: {
          formatter: "Price: {c}",
        },
        data: [
          [
            {
              tooltip: { show: false },
              x: 240,
              coord: [1, props.priceSalesData.current_price],
              symbol: "arrow",
              symbolSize: 8,
              lineStyle: {
                color: "#eb3c96",
              },
              format: "Current Price",
              label: {
                position: "middle",
                rotate: 0,
                formatter: () => {
                  return `${
                    Math.round(
                      (10000 *
                        (props.priceSalesData.new_price -
                          props.priceSalesData.current_price)) /
                        props.priceSalesData.current_price
                    ) / 100
                  } %`;
                },
              },
            },
            {
              x: 240,
              coord: [0, props.priceSalesData.new_price],
              symbolSize: 8,
              symbol: "arrow",
            },
          ],
          [
            {
              tooltip: { formatter: "Floor_Price: {c}" },
              x: 80,
              coord: [1, props.priceSalesData.floor_price],
              lineStyle: {
                color: "green",
              },
              label: {
                position: "start",
                formatter: "Floor Price",
              },
              value: props.priceSalesData.floor_price,
            },
            {
              coord: ["After", props.priceSalesData.floor_price],
              symbol: "none",
            },
          ],
          [
            {
              tooltip: { formatter: "NHIA Price: {c}" },
              x: 80,
              value: props.priceSalesData.NHIA_price,
              coord: [0, props.priceSalesData.NHIA_price],
              lineStyle: {
                color: "black",
              },
              label: {
                position: "start",
                formatter: "NHIA Price",
              },
            },
            {
              coord: ["After", props.priceSalesData.NHIA_price],
              symbol: "none",
            },
          ],
          [
            {
              tooltip: { show: false },
              x: 120,
              coord: [0, props.priceSalesData.new_price],
              symbol: "arrow",
              symbolSize: 8,
              lineStyle: {
                color: "#eb3c96",
              },
              label: {
                position: "middle",
                rotate: 0,
                formatter: () => {
                  return `${
                    Math.round(
                      (10000 *
                        (props.priceSalesData.new_price -
                          props.priceSalesData.NHIA_price)) /
                        props.priceSalesData.NHIA_price
                    ) / 100
                  } %`;
                },
              },
            },
            {
              x: 120,
              symbol: "arrow",
              symbolSize: 8,
              coord: [0, props.priceSalesData.NHIA_price],
            },
          ],
          [
            {
              tooltip: { show: false },
              coord: [1, props.priceSalesData.NHIA_price],
              symbol: "arrow",
              symbolSize: 8,
              lineStyle: {
                color: "#eb3c96",
              },
              label: {
                position: "middle",
                rotate: 0,
                formatter: () => {
                  return `${
                    Math.round(
                      (10000 *
                        (props.updateClients[props.checkedIndex]
                          .negotiatedPrice -
                          props.priceSalesData.NHIA_price)) /
                        props.priceSalesData.NHIA_price
                    ) / 100
                  } %`;
                },
              },
            },
            {
              symbol: "arrow",
              symbolSize: 8,
              coord: [
                1,
                props.updateClients[props.checkedIndex].negotiatedPrice,
              ],
            },
          ],
          [
            {
              tooltip: { formatter: "Lowest Price: {c}" },
              x: 80,
              value: props.priceSalesData.lowest_price,
              coord: [0, props.priceSalesData.lowest_price],
              lineStyle: {
                color: "red",
              },
              label: {
                position: "start",
                formatter: "Lowest Price",
              },
            },
            {
              coord: ["After", props.priceSalesData.lowest_price],
              symbol: "none",
            },
          ],
          [
            {
              x: 80,
              tooltip: { formatter: "Current Price: {c}" },
              value: props.priceSalesData.current_price.toFixed(2),
              coord: [0, props.priceSalesData.current_price],
              lineStyle: {
                color: "purple",
              },
              label: {
                position: "start",
                formatter: "Current Price",
              },
            },
            {
              coord: ["Before", props.priceSalesData.current_price],
              symbol: "none",
            },
          ],
          [
            {
              tooltip: { formatter: "New Price: {c}" },
              value: props.priceSalesData.new_price.toFixed(2),
              x: 80,
              coord: [0, props.priceSalesData.new_price],
              lineStyle: {
                color: "blue",
              },
              label: {
                position: "start",
                formatter: "New Price",
              },
            },
            {
              coord: ["After", props.priceSalesData.new_price],
              symbol: "none",
            },
          ],
        ],
      },
    },
  ],
}));
</script>
