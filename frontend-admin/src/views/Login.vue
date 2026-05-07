<template>
  <div class="login-container">
    <!-- 背景装饰 -->
    <div class="bg-decoration bg-decoration-1"></div>
    <div class="bg-decoration bg-decoration-2"></div>
    <div class="bg-decoration bg-decoration-3"></div>

    <!-- 登录卡片 -->
    <div class="login-card">
      <!-- 顶部图标 -->
      <div class="card-icon">
        <div class="icon-box">
          <el-icon><check /></el-icon>
        </div>
      </div>

      <!-- 标题 -->
      <div class="card-title">
        <h1>证券交易系统</h1>
        <p>专业的证券交易平台</p>
      </div>

      <!-- 登录表单 -->
      <el-form
        ref="formRef"
        :model="loginForm"
        :rules="rules"
        @keyup.enter="handleLogin"
      >
        <!-- 用户名 -->
        <el-form-item prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="请输入用户名"
            clearable
          >
            <template #prefix>
              <el-icon><user /></el-icon>
            </template>
          </el-input>
        </el-form-item>

        <!-- 密码 -->
        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="请输入密码"
            clearable
            show-password
          >
            <template #prefix>
              <el-icon><lock /></el-icon>
            </template>
          </el-input>
        </el-form-item>

        <!-- 登录按钮 -->
        <el-button
          type="primary"
          size="large"
          class="login-btn"
          :loading="loading"
          @click="handleLogin"
        >
          登录
        </el-button>
      </el-form>

      <!-- 底部提示 -->
      <div class="card-footer">
        <p class="demo-tip">演示账号: <span>admin</span> / <span>123456</span></p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { authAPI } from '@/utils/api'
import { ElMessage, FormInstance } from 'element-plus'
import { Check, User, Lock } from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()
const formRef = ref<FormInstance>()
const loading = ref(false)

const loginForm = reactive({
  username: '',
  password: '',
  remember: false,
})

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' },
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度在 6 到 20 个字符', trigger: 'blur' },
  ],
}

const handleLogin = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) return

    loading.value = true

    try {
      const response: any = await authAPI.login(loginForm.username, loginForm.password)
      
      if (response.code === 200) {
        const { user, token } = response.data
        localStorage.setItem('token', token)
        localStorage.setItem('userId', user.id)
        userStore.setUser(user)
        ElMessage.success('登录成功')
        router.push('/market')
      } else {
        ElMessage.error(response.message || '登录失败')
      }
    } catch (error: any) {
      const errorMessage = error.response?.data?.message || '登录失败，请重试'
      ElMessage.error(errorMessage)
    } finally {
      loading.value = false
    }
  })
}
</script>

<style scoped lang="scss">
.login-container {
  width: 100%;
  height: 100vh;
  background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 50%, #90caf9 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  position: relative;
}

// 背景装饰
.bg-decoration {
  position: absolute;
  border-radius: 50%;
  opacity: 0.1;
  pointer-events: none;
}

.bg-decoration-1 {
  width: 400px;
  height: 400px;
  background: #0066cc;
  top: -100px;
  left: -100px;
}

.bg-decoration-2 {
  width: 300px;
  height: 300px;
  background: #0066cc;
  bottom: -50px;
  right: -50px;
}

.bg-decoration-3 {
  width: 200px;
  height: 200px;
  background: #0066cc;
  top: 50%;
  right: 10%;
  opacity: 0.05;
}

// 登录卡片
.login-card {
  width: 100%;
  max-width: 420px;
  background: white;
  border-radius: 12px;
  padding: 50px 40px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 10;
}

// 顶部图标
.card-icon {
  display: flex;
  justify-content: center;
  margin-bottom: 24px;
}

.icon-box {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #0066cc 0%, #0052a3 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 32px;
  box-shadow: 0 4px 12px rgba(0, 102, 204, 0.3);
}

// 标题
.card-title {
  text-align: center;
  margin-bottom: 32px;

  h1 {
    font-size: 24px;
    font-weight: 600;
    color: #1a1a1a;
    margin: 0 0 8px 0;
  }

  p {
    font-size: 12px;
    color: #999999;
    margin: 0;
  }
}

// 表单
:deep(.el-form-item) {
  margin-bottom: 16px;

  .el-input__wrapper {
    background-color: #f5f7fa;
    border: 1px solid #e8e8e8;
    border-radius: 6px;
    transition: all 0.3s ease;

    &:hover {
      border-color: #0066cc;
      background-color: #ffffff;
    }

    &.is-focus {
      border-color: #0066cc;
      background-color: #ffffff;
      box-shadow: 0 0 0 2px rgba(0, 102, 204, 0.1);
    }
  }

  .el-input__inner {
    background-color: transparent;
    color: #1a1a1a;
    font-size: 14px;

    &::placeholder {
      color: #999999;
    }
  }

  .el-icon {
    color: #999999;
  }
}

// 表单底部
.form-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  font-size: 12px;

  :deep(.el-checkbox) {
    .el-checkbox__label {
      color: #666666;
    }
  }

  .forgot-password {
    color: #0066cc;
    text-decoration: none;
    transition: all 0.3s ease;

    &:hover {
      color: #0052a3;
      text-decoration: underline;
    }
  }
}

// 登录按钮
.login-btn {
  width: 100%;
  height: 40px;
  font-size: 16px;
  font-weight: 500;
  border-radius: 6px;
  background: linear-gradient(135deg, #0066cc 0%, #0052a3 100%);
  border: none;
  transition: all 0.3s ease;

  &:hover {
    box-shadow: 0 4px 12px rgba(0, 102, 204, 0.3);
    transform: translateY(-2px);
  }

  &:active {
    transform: translateY(0);
  }
}

// 卡片底部
.card-footer {
  text-align: center;
  margin-top: 24px;
  padding-top: 16px;
  border-top: 1px solid #f0f0f0;

  .demo-tip {
    font-size: 12px;
    color: #999999;
    margin: 0;

    span {
      color: #0066cc;
      font-weight: 500;
    }
  }
}

// 响应式设计
@media (max-width: 480px) {
  .login-card {
    max-width: 100%;
    margin: 0 16px;
    padding: 40px 24px;
  }

  .card-title {
    margin-bottom: 24px;

    h1 {
      font-size: 20px;
    }
  }

  .form-footer {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }

  .bg-decoration {
    display: none;
  }
}
</style>
