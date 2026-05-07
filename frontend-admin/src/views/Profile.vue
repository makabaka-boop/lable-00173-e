<template>
  <div class="profile-container">
    <div class="profile-header">
      <h1>个人资料</h1>
    </div>

    <div class="profile-content">
      <!-- 基本信息卡片 -->
      <div class="profile-card">
        <div class="card-header">
          <h2>基本信息</h2>
          <el-button 
            v-if="!isEditing" 
            type="primary" 
            size="small" 
            @click="startEdit"
          >
            编辑
          </el-button>
          <div v-else class="edit-actions">
            <el-button size="small" @click="cancelEdit">取消</el-button>
            <el-button type="primary" size="small" @click="saveProfile">保存</el-button>
          </div>
        </div>

        <div class="card-body">
          <el-form :model="profileForm" label-width="100px" class="profile-form">
            <el-row :gutter="20">
              <el-col :xs="24" :sm="12">
                <el-form-item label="用户名">
                  <el-input 
                    v-if="isEditing" 
                    v-model="profileForm.name" 
                    placeholder="请输入用户名"
                  />
                  <span v-else>{{ profileForm.name || '-' }}</span>
                </el-form-item>
              </el-col>
              <el-col :xs="24" :sm="12">
                <el-form-item label="邮箱">
                  <el-input 
                    v-if="isEditing" 
                    v-model="profileForm.email" 
                    type="email"
                    placeholder="请输入邮箱"
                  />
                  <span v-else>{{ profileForm.email || '-' }}</span>
                </el-form-item>
              </el-col>
            </el-row>

            <el-row :gutter="20">
              <el-col :xs="24" :sm="12">
                <el-form-item label="手机号">
                  <el-input 
                    v-if="isEditing" 
                    v-model="profileForm.phone" 
                    placeholder="请输入手机号"
                  />
                  <span v-else>{{ profileForm.phone || '-' }}</span>
                </el-form-item>
              </el-col>
              <el-col :xs="24" :sm="12">
                <el-form-item label="注册时间">
                  <span>{{ formatDate(userStore.user?.createdAt || Date.now()) }}</span>
                </el-form-item>
              </el-col>
            </el-row>

            <el-form-item label="地址">
              <el-input 
                v-if="isEditing" 
                v-model="profileForm.address" 
                type="textarea"
                :rows="2"
                placeholder="请输入地址"
              />
              <span v-else>{{ profileForm.address || '-' }}</span>
            </el-form-item>

            <el-form-item label="个人简介">
              <el-input 
                v-if="isEditing" 
                v-model="profileForm.bio" 
                type="textarea"
                :rows="3"
                placeholder="请输入个人简介"
              />
              <span v-else>{{ profileForm.bio || '-' }}</span>
            </el-form-item>
          </el-form>
        </div>
      </div>

      <!-- 账户信息卡片 -->
      <div class="profile-card">
        <div class="card-header">
          <h2>账户信息</h2>
        </div>
        <div class="card-body">
          <div class="account-stats">
            <div class="stat-item">
              <div class="stat-label">总资产</div>
              <div class="stat-value">{{ formatCurrency(userStore.user?.totalAssets || 0) }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-label">持仓数量</div>
              <div class="stat-value">{{ userStore.positions.length }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-label">用户ID</div>
              <div class="stat-value">{{ userStore.user?.id || '-' }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { userAPI } from '@/utils/api'
import { formatCurrency, formatDate } from '@/utils/format'
import { ElMessage } from 'element-plus'
import type { User } from '@/types'

const userStore = useUserStore()
const isEditing = ref(false)

const profileForm = reactive({
  name: '',
  email: '',
  phone: '',
  address: '',
  bio: '',
  avatar: '',
})

const startEdit = () => {
  if (userStore.user) {
    profileForm.name = userStore.user.name
    profileForm.email = userStore.user.email
    profileForm.phone = userStore.user.phone || ''
    profileForm.address = userStore.user.address || ''
    profileForm.bio = userStore.user.bio || ''
    profileForm.avatar = userStore.user.avatar || ''
  }
  isEditing.value = true
}

const cancelEdit = () => {
  isEditing.value = false
}

const saveProfile = async () => {
  if (!profileForm.name || !profileForm.email) {
    ElMessage.error('请填写必填项')
    return
  }

  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(profileForm.email)) {
    ElMessage.error('请输入正确的邮箱地址')
    return
  }

  if (profileForm.phone && !/^1[3-9]\d{9}$/.test(profileForm.phone)) {
    ElMessage.error('请输入正确的手机号')
    return
  }

  try {
    const userId = localStorage.getItem('userId')
    const response = await userAPI.updateProfile(parseInt(userId || '1'), {
      name: profileForm.name,
      email: profileForm.email,
      phone: profileForm.phone,
      address: profileForm.address,
      bio: profileForm.bio,
      avatar: profileForm.avatar,
    })

    if (response.code === 200) {
      userStore.setUser(response.data)
      ElMessage.success('保存成功')
      isEditing.value = false
    } else {
      ElMessage.error(response.message || '保存失败')
    }
  } catch (error) {
    ElMessage.error('保存失败，请重试')
  }
}

onMounted(async () => {
  try {
    const userId = localStorage.getItem('userId')
    if (userId) {
      const response = await userAPI.getProfile(parseInt(userId))
      if (response.code === 200) {
        const user = response.data
        userStore.setUser(user)
        profileForm.name = user.name
        profileForm.email = user.email
        profileForm.phone = user.phone || ''
        profileForm.address = user.address || ''
        profileForm.bio = user.bio || ''
        profileForm.avatar = user.avatar || ''
      }
    }
  } catch (error) {
    console.error('Failed to fetch user profile:', error)
  }
})
</script>

<style scoped lang="scss">
.profile-container {
  padding: 24px;
}

.profile-header {
  margin-bottom: 24px;

  h1 {
    font-size: 28px;
    font-weight: 600;
    color: var(--el-text-color-primary);
  }
}

.profile-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.profile-card {
  background: var(--el-bg-color);
  border: 1px solid var(--el-border-color-light);
  border-radius: 8px;
  padding: 24px;
  box-shadow: var(--shadow-sm);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--el-border-color-light);

  h2 {
    font-size: 18px;
    font-weight: 600;
    color: var(--el-text-color-primary);
    margin: 0;
  }
}

.edit-actions {
  display: flex;
  gap: 8px;
}

.card-body {
  .profile-form {
    :deep(.el-form-item__label) {
      color: var(--el-text-color-regular);
      font-weight: 500;
    }

    :deep(.el-form-item) {
      margin-bottom: 20px;
    }

    span {
      color: var(--el-text-color-primary);
      font-size: 14px;
    }
  }
}

.account-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 24px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 16px;
  background: var(--el-fill-color-lighter);
  border-radius: 6px;

  .stat-label {
    font-size: 12px;
    color: var(--el-text-color-regular);
  }

  .stat-value {
    font-size: 20px;
    font-weight: 600;
    color: var(--el-text-color-primary);
  }
}

@media (max-width: 768px) {
  .profile-container {
    padding: 16px;
  }

  .profile-card {
    padding: 16px;
  }

  .account-stats {
    grid-template-columns: 1fr;
  }
}
</style>
