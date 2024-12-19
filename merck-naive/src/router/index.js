import { createRouter, createWebHistory } from 'vue-router'
import Login from '../components/Login.vue'
import Svp from '../components/Svp.vue'  


const isLoggedIn = async () => {
  try {
    const response = await fetch('/api/users/me/', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    });

    if (response.ok) {
      return true;
    } else {
      return false;
    }
  } catch (error) {
    console.error('Error checking login status:', error);
    return false;
  }
}

const routes = [
  {
    path: '/login',
    name: 'login',
    component: Login
  },
  {
    path: '/',
    name: 'svp',
    component: Svp
  },
  // 其他需要保護的路由可以添加到這裡
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, from, next) => {
  // 如果訪問的是 /login 或以 /api 開頭的路徑，無需檢查登錄
  if (to.path === '/login' || to.path.startsWith('/api')) {
    next(); // 直接放行
  } else {
    const loggedIn = await isLoggedIn();
    
    if (loggedIn) {
      next(); // 已登錄，放行
    } else {
      next('/login'); // 未登錄，跳轉到 login 頁面
      //next();
    }
  }
});

export default router
