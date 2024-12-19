<!-- src/components/Login.vue -->
<template>
  <n-config-provider :theme="darkTheme">
    <n-card title="Login" hoverable style="border-radius: 5%">
      <n-form
        ref="form"
        :model="form"
        :rules="rules"
        aria-label="登入表單"
        label-position="top"
        label-width="80px"
      >
        <n-form-item label="Username" path="username">
          <n-input
            v-model:value="form.username"
            placeholder="Please input Username"
          />
        </n-form-item>

        <n-form-item label="Password" path="password">
          <n-input
            v-model:value="form.password"
            type="password"
            placeholder="Please input Password"
          />
        </n-form-item>

        <n-form-item class="flex justify-center">
          <n-button keyboard type="primary" @click="handleLogin"
            >Login</n-button
          >
        </n-form-item>
        <n-form-item class="flex justify-center">
          {{ errorMessage }}
        </n-form-item>
      </n-form>
    </n-card>
  </n-config-provider>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import { useRouter } from "vue-router";
import apiClient from "../api/axio";
import { NForm, NFormItem, NInput, NButton, darkTheme } from "naive-ui";

// 定義表單的數據結構
interface LoginForm {
  username: string;
  password: string;
}

export default defineComponent({
  name: "Login",
  components: {
    NForm,
    NFormItem,
    NInput,
    NButton,
  },
  setup() {
    const router = useRouter();
    const form = ref<LoginForm>({
      username: "",
      password: "",
    });
    const rules = {
      email: {
        required: true,
        message: "Pleaser Enter Username",
        trigger: "blur",
      },
      password: {
        required: true,
        message: "Pleaser Enter Pssword",
        trigger: "blur",
      },
    };

    const errorMessage = ref("");

    const handleLogin = async () => {
      try {
        if (form.value.username && form.value.password) {
          const response = await apiClient.post(
            "/token",
            {
              username: form.value.username,
              password: form.value.password,
            },
            {
              headers: {
                "Content-Type": "application/x-www-form-urlencoded",
              },
            }
          );
          if (response.status === 200) {
            const data = response.data;
            console.log(data.access_token);
            const token = data.access_token;
            localStorage.setItem("token", token);
            router.push("/");
          }
        }
      } catch (error) {
        console.error("登入失敗:", error);
        errorMessage.value = "Login Failed";
      }
    };
    return {
      form,
      rules,
      handleLogin,
      darkTheme,
      errorMessage,
    };
  },
});
</script>

<style scoped>
.flex {
  display: flex;
}
.justify-center {
  justify-content: center;
}
</style>
