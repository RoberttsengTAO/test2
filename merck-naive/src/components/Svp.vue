<template>
  <div class="page-content">
    <n-theme-editor>
      <n-config-provider
        :theme="lightTheme"
        :theme-overrides="lightThemeOverrides"
        :font-family="'verdana'"
      >
        <n-global-style />
        <n-page-header title="SVP Emulator"></n-page-header>
        <n-layout
          style="
            min-height: 90vh;
            max-height: 100vh;
            width: 90vw;
            position: absolute;
            top: 5vh;
            left: 5vw;
            overflow: auto;
          "
        >
          <n-h1 align="left"
            >SVP Simulation
            <n-button type="success" @click="logout">logout</n-button>
          </n-h1>

          <n-layout-header style="height: 8vh; padding: 0; margin: 0">
            <!-- Header Section -->
            <n-space align="start">
              <n-h3>Product Name:</n-h3>
              <n-select
                v-model:value="selectedProduct"
                :options="productOptions"
                placeholder="Choose Product"
                style="width: 450px"
                :disabled="!isclientinput"
              />
            </n-space>
          </n-layout-header>
          <n-layout has-sider>
            <n-layout-sider :width="isclientinput ? '33%' : '50%'">
              <n-card
                :align="isclientinput ? 'left' : 'center'"
                style="margin-top: 8px"
                :bordered="false"
              >
                <PriceChart
                  v-if="!isclientinput"
                  :priceSalesData="price_sales_data"
                  :updateClients="updateClients"
                  :checkedIndex="checkedindex"
                />
                <n-data-table
                  v-if="isclientinput"
                  :columns="clientColumns"
                  :data="filteredClients"
                  :bordered="false"
                  :pagination="{ pageSize: 13 }"
                  striped
                />
              </n-card>
            </n-layout-sider>
            <n-layout-content
              style="margin-top: 0; padding-top: 0"
              content-style="padding: 4px;"
            >
              <n-card align="left" style="margin-top: 2px" :bordered="false">
                <n-h3 align="left" v-if="isclientinput"
                  >Current Customer
                  <n-button
                    text
                    style="font-size: 18px"
                    v-if="isclientinput"
                    @click="clearClientRow"
                  >
                    <n-icon>
                      <Refresh />
                    </n-icon>
                  </n-button>
                </n-h3>

                <n-divider style="margin-top: 2px" v-if="isclientinput" />
                <n-data-table
                  v-if="isclientinput"
                  :max-height="180"
                  :scroll-x="true"
                  :columns="CurrentClientFormcolumns"
                  :data="updateClients"
                />

                <SalesChart
                  v-if="!isclientinput"
                  :priceSalesData="price_sales_data"
                />
              </n-card>

              <n-card
                v-if="isclientinput"
                align="left"
                :title="isclientinput ? 'New Customer' : ''"
                style="margin-top: 20px"
                :bordered="false"
              >
                <n-divider style="margin-top: 2px" />
                <n-form v-if="isclientinput">
                  <n-space justify="start">
                    <n-form-item label="Proposed Negotiated Price">
                      <n-input-number
                        v-model:value="newClientProposedPrice"
                        placeholder="Proposed Negotiated Price"
                        :min="0"
                      />
                    </n-form-item>
                    <n-form-item label="Proposed Target(Std. Unit)">
                      <n-input-number
                        v-model:value="newClientProposedTarget"
                        placeholder="Proposed Current Target"
                        :min="0"
                      />
                    </n-form-item>
                  </n-space>
                </n-form>
              </n-card>
            </n-layout-content>
          </n-layout>
          <n-layout-footer>
            <!-- Simulate Button -->
            <n-space justify="end" style="margin-top: 20px; margin-right: 40px">
              <n-button
                type="primary"
                :disabled="selectedProduct === null"
                @click="simulate"
                size="large"
                style="background-color: #ff69b4; color: white"
              >
                {{ simulateButtonLabel }}
              </n-button>
            </n-space>
          </n-layout-footer>
        </n-layout>
      </n-config-provider>
    </n-theme-editor>
  </div>
</template>

<script setup lang="ts">
import PriceChart from "./SvpPriceChart.vue";
import SalesChart from "./SvpSalesChart.vue";
import { ref, onMounted, h, watch, provide } from "vue";
import {
  NIcon,
  lightTheme,
  NLayout,
  NSpace,
  NSelect,
  NCard,
  NInputNumber,
  NButton,
  NConfigProvider,
  NThemeEditor,
  NCheckbox,
} from "naive-ui";

import type { DataTableColumns } from "naive-ui";
import Papa from "papaparse";
import { AddOutline, Remove, Refresh } from "@vicons/ionicons5";
import { THEME_KEY } from "vue-echarts";
import { use } from "echarts/core";
import { BarChart } from "echarts/charts";
import { useRouter } from "vue-router";
import {
  MarkLineComponent,
  MarkPointComponent,
  TitleComponent,
  TooltipComponent,
  GridComponent,
  DatasetComponent,
  LegendComponent,
  ToolboxComponent,
  DataZoomComponent,
} from "echarts/components";
import { CanvasRenderer } from "echarts/renderers";

use([
  MarkLineComponent,
  MarkPointComponent,
  TitleComponent,
  TooltipComponent,
  GridComponent,
  BarChart,
  DatasetComponent,
  LegendComponent,
  CanvasRenderer,
  ToolboxComponent,
  DataZoomComponent,
]);
provide(THEME_KEY, "light");
const lightThemeOverrides = {
  common: {
    bodyColor: "#ffffff",
    cardColor: "#ffffff",
    iconColor: "#0f69af",
  },
  Input: {
    color: "rgba(255, 220, 185, 1)",
    textColor: "rgba(27, 29, 31, 1)",
    iconColor: "rgba(27, 29, 31, 1)",
    suffixTextColor: "rgba(0, 0, 0, 1)",
    textColorDisabled: "rgba(141, 141, 141, 1)",
    colorDisabled: "rgba(191, 191, 191, 1)",
  },
  Button: {
    heightLarge: "70px",
    weightLarge: "200px",
    borderRadiusLarge: "20px",
    fontSizeLarge: "22px",
  },
  DataTable: {
    tdColorStriped: "#f2f2f2",
  },
  Divider: {
    color: "rgba(255, 255, 255, 1)",
  },
  Select: {
    peers: {
      InternalSelection: {
        placeholderColor: "rgba(54, 54, 73, 1)",
        textColor: "rgba(27, 29, 31, 1)",
        color: "rgba(255, 220, 185, 1)",
      },
    },
  },
};

interface ClientData {
  BU: string;
  client: string;
  currentAspPrice: number;
  targetQty: number;
  averageCurrentPrice: number;
  cosmosPrice: number;
  product: string;
  NHIA_Price: number;
}

interface CurrenClientData {
  key: number;
  client: string;
  currentAspPrice: number;
  negotiatedPrice: number;
  targetQty: number;
  targetAdjustment: number;
}

interface PriceData {
  current_sales: number;
  new_sales: number;
  current_price: number;
  new_price: number;
  totalQty: number;
  floor_price: number;
  lowest_price: number;
  highest_price: number;
  NHIA_price: number;
  averageCurrentPrice: number;
}

const price_sales_data = ref<PriceData>({
  current_sales: 0,
  new_sales: 0,
  current_price: 0,
  new_price: 0,
  totalQty: 0,
  floor_price: 0,
  lowest_price: 0,
  highest_price: 0,
  NHIA_price: 0,
  averageCurrentPrice: 0,
});

function createData(): CurrenClientData[] {
  return [];
}
const updateClients = ref(createData());

const createColumns = (): DataTableColumns<CurrenClientData> => [
  {
    title: "",
    key: "plus",
    fixed: "left",
    width: 80,
    render(index) {
      return h(
        NButton,
        {
          icon: () => h(NIcon, null, { default: () => h(AddOutline) }),
          onClick(): void {
            console.log("index", index);
            clientOptions.value.length >= 0 &&
            updateClients.value.length < filteredClients.value.length
              ? addClientRow()
              : console.log("No clients available");
          },
        },
        { default: () => "+" }
      );
    },
  },
  {
    title: "Customer",
    key: "client",
    width: "20vh",
    resizable: true,
    minWidth: 120,
    render(row, index) {
      return h(NSelect, {
        value: row.client,
        placeholder: "",
        filterable: true,
        options: clientOptions.value,

        onUpdateValue(v) {
          clientOptions.value = clientOptions.value.filter(
            (client) => client.value !== v
          );
          if (updateClients.value[index].client !== "") {
            clientOptions.value.push({
              label: updateClients.value[index].client,
              value: updateClients.value[index].client,
            });
          }
          updateClients.value[index].client = v;
          const clientIndex = filteredClients.value.findIndex(
            (client) => client.client === v
          );
          const selectedClient = filteredClients.value[clientIndex];
          updateClients.value[index].currentAspPrice = Number(
            selectedClient.currentAspPrice
          );
          updateClients.value[index].negotiatedPrice = Number(
            selectedClient.currentAspPrice
          );
          updateClients.value[index].targetQty = Number(
            selectedClient.targetQty
          );
        },
      });
    },
  },
  {
    title: "Current Price",
    key: "currentAspPrice",
    render(row, index) {
      return h(NInputNumber, {
        readonly: true,
        disabled: true,
        showButton: false,
        value: row.currentAspPrice,
        onUpdateValue(v) {
          updateClients.value[index].currentAspPrice = v;
        },
      });
    },
  },
  {
    title: "Negotiated Price",
    key: "negotiatedPrice",

    render(row, index) {
      return h(NInputNumber, {
        showButton: false,
        value: row.negotiatedPrice,
        min: 0,
        onUpdateValue(v) {
          updateClients.value[index].negotiatedPrice = v;
        },
      });
    },
  },
  {
    title: "Price percentage",
    key: "price_percentage",
    render(row, index) {
      return h(
        NInputNumber,
        {
          readonly: true,
          disabled: true,
          showButton: false,
          value:
            Math.round(
              (10000 * (row.negotiatedPrice - row.currentAspPrice)) /
                row.currentAspPrice
            ) / 100,

          onUpdateValue(v) {
            updateClients.value[index].currentAspPrice = v;
          },
        },
        { suffix: () => "%" }
      );
    },
  },
  {
    title: "Current Target(Std. Unit)",
    key: "targetQty",
    render(row, index) {
      return h(NInputNumber, {
        value: row.targetQty,
        showButton: false,
        disabled: true,
        onUpdateValue(v) {
          if (updateClients.value && updateClients.value[index]) {
            updateClients.value[index].targetQty = v;
          } else {
            console.error(
              "Unable to update targetQty: Invalid index or updateClients is null"
            );
          }
        },
      });
    },
  },
  {
    title: "Target Unit adj",
    key: "targetAdjustment",
    render(row, index) {
      return h(
        NInputNumber,
        {
          value: row.targetAdjustment,
          showButton: false,
          suffix: "%",
          onUpdateValue(v) {
            updateClients.value[index].targetAdjustment = v;
          },
        },
        { suffix: () => "%" }
      );
    },
  },
  {
    title: "",
    key: "checkbox",
    fixed: "right",
    width: 50,
    render(row, index) {
      return h(NCheckbox, {
        checked: index === checkedindex.value ? true : false,
        onClick(): void {
          console.log("row", row);
          checkedindex.value = index;
        },
      });
    },
  },
  {
    title: "",
    key: "minus",
    width: 50,
    render(row, index) {
      return h(
        NButton,
        {
          icon: () => h(NIcon, null, { default: () => h(Remove) }), // 添加圖標
          onClick(): void {
            console.log("row", row);
            removeClientRow(index);
          },
        },
        { default: () => "-" }
      );
    },
  },
];

const addClientRow = () => {
  updateClients.value.push({
    key: updateClients.value.length,
    client: "",
    currentAspPrice: 1000,
    negotiatedPrice: 1000,
    targetQty: 1000,
    targetAdjustment: 0,
  });
};
const currentClients = ref<ClientData[]>([]);
const selectedProduct = ref<string | null>(null);
const productOptions = ref<{ label: string; value: string }[]>([]);
const clientOptions = ref<{ label: string; value: string }[]>([]);
const clientColumns = [
  { title: "Customer", key: "client" },
  {
    title: "Curren Price (TWD)",
    key: "currentAspPrice",
    sorter: (row1, row2) => row1.currentAspPrice - row2.currentAspPrice,
    defaultSortOrder: "descend",
  },
  {
    title: "Target (Std. Unit)",
    key: "targetQty",
    sorter: (row1, row2) => row1.targetQty - row2.targetQty,
  },
];
const CurrentClientFormcolumns = createColumns();
const newClientProposedPrice = ref(0);
const newClientProposedTarget = ref(0);
const leftCardTitle = ref("Client List");
const checkedindex = ref(0);

const removeClientRow = (index) => {
  if (index === 0) return false;
  console.log("index", index);
  clientOptions.value.push({
    label: updateClients.value[index].client,
    value: updateClients.value[index].client,
  });
  if (checkedindex.value === index) {
    checkedindex.value = 0;
  }
  updateClients.value.splice(index, 1);
};
const clearClientRow = () => {
  updateClients.value = [];
  addClientRow();
  clientOptions.value = filteredClients.value.map((client) => ({
    label: client.client,
    value: client.client,
  }));
};
const sales_minprice_data = ref({
  currentSales: 0,
  newSales: 0,
  minPrice: Infinity,
  maxPrice: 0,
  totalQty: 0,
  totalorQty:0,
  averageCurrentPrice: 0,
});
const isclientinput = ref(true);
const simulateButtonLabel = ref("Simulate");

const simulate = () => {
  sales_minprice_data.value = filteredClients.value.reduce(
    (result, a) => {
      const updatedClient = updateClients.value.find(
        (b) => b.client === a.client
      );
      const negotiatedPrice =
        updatedClient?.negotiatedPrice ?? a.currentAspPrice;
      const currentAspPrice =
        updatedClient?.currentAspPrice ?? a.currentAspPrice;
      const targetQty: number = updatedClient
        ? updatedClient.targetQty *
          (1 + 0.01 * (updatedClient.targetAdjustment ?? 0))
        : Number(a.targetQty);
      const or_targetQty: number = updatedClient
        ? updatedClient.targetQty
        : Number(a.targetQty);
      result.totalQty += targetQty;
      result.totalorQty += or_targetQty;
      result.averageCurrentPrice = a.averageCurrentPrice;
      result.minPrice = Math.min(result.minPrice, a.currentAspPrice);
      result.maxPrice = Math.max(result.maxPrice, negotiatedPrice);
      result.currentSales += currentAspPrice * or_targetQty;
      result.newSales += negotiatedPrice * targetQty;
      return result;
    },
    {
      originQty: 0,
      currentSales: 0,
      newSales: 0,
      minPrice: Infinity,
      totalQty: 0,
      totalorQty: 0,
      maxPrice: 0,
      averageCurrentPrice: 0,
    }
  );

  price_sales_data.value.current_sales = sales_minprice_data.value.currentSales;
  price_sales_data.value.new_sales =
    sales_minprice_data.value.newSales +
    newClientProposedPrice.value * newClientProposedTarget.value;
  price_sales_data.value.totalQty = sales_minprice_data.value.totalQty;
  price_sales_data.value.lowest_price = sales_minprice_data.value.minPrice;
  price_sales_data.value.highest_price = Math.max(
    sales_minprice_data.value.maxPrice,
    newClientProposedPrice.value,
    filteredClients.value[0].NHIA_Price
  );
  price_sales_data.value.current_price = 
    sales_minprice_data.value.currentSales / sales_minprice_data.value.totalorQty;
  price_sales_data.value.new_price =
    price_sales_data.value.new_sales /
    (price_sales_data.value.totalQty + newClientProposedTarget.value);
  price_sales_data.value.floor_price = Number(
    filteredClients.value[0].cosmosPrice
  );
  price_sales_data.value.NHIA_price = Number(
    filteredClients.value[0].NHIA_Price
  );

  console.log("price_data:", price_sales_data.value);
  isclientinput.value = !isclientinput.value;
  simulateButtonLabel.value =
    simulateButtonLabel.value === "Simulate" ? "Re-Simulate" : "Simulate";
  leftCardTitle.value =
    leftCardTitle.value === "Client List" ? "" : "Client List";
  console.log("isclientinput:", isclientinput.value);
};

//const csvFilePath = "../sample/sample.csv";
const csvFilePath = "/api/static/sample.csv";
const loadCsvData = async () => {
  try {
    const response = await fetch(csvFilePath);
    const csvData = await response.text();

    Papa.parse(csvData, {
      header: true,
      skipEmptyLines: true,
      complete: (result) => {
        currentClients.value = result.data
          .map((row) => ({
            BU: row.BU,
            client: row.Client,
            currentAspPrice: row["Current ASP Price"],
            targetQty: row["Target QTY"],
            averageCurrentPrice: row["Average Current Price"],
            cosmosPrice: row["COSMOS Price"],
            product: row["Product"],
            NHIA_Price: row["NHIA Price"],
          }))
          .filter(
            (item) =>
              item.BU === user_business_unit.value ||
              user_business_unit.value === "admin"
          );
        const uniqueProducts = Array.from(
          new Set(currentClients.value.map((item) => item.product))
        );
        productOptions.value = uniqueProducts.map((product) => ({
          label: product,
          value: product,
        }));
      },
    });
    console.log("CSV Data:", currentClients.value);
    console.log("opt Data:", productOptions.value);
    console.log("client Data:", clientOptions.value);
  } catch (error) {
    console.error("Error loading CSV file:", error);
  }
};
const user_business_unit = ref("admin");
const get_user_business_unit = async () => {
  try {
    const response = await fetch("/api/users/me/", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`, // 假設 token 存儲在 localStorage
      },
    });
    const data = await response.json();
    user_business_unit.value = data.role;
    console.log(user_business_unit.value);
    loadCsvData();
  } catch (error) {
    console.error("Error fetching user business unit:", error);
  }
};
const filteredClients = ref([]);
const router = useRouter();
const logout = () => {
  localStorage.removeItem("token");
  router.push("/login");
};
watch(selectedProduct, (newProduct) => {
  if (!newProduct) {
    filteredClients.value = [];
  } else {
    filteredClients.value = currentClients.value.filter(
      (client) => client.product === newProduct
    );
    clearClientRow();
  }
});

onMounted(() => {
  addClientRow();
  get_user_business_unit();
});
</script>

<style scoped>
.chart-container {
  height: 50vh;
  width: 50vw;
  border-radius: 10px;
  overflow: hidden;
  padding: 20px;
}

.chart {
  height: 50vh;
  width: 40vw;
  overflow: hidden;
}

.n-layout-header,
.n-layout-content,
.n-layout-footer {
  background: hsl(0, 0%, 100%);
  padding: 24px;
}
</style>
