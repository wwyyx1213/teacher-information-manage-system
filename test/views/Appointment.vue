<template>
  <div class="max-w-xl mx-auto mt-10 p-6 bg-white rounded-2xl shadow">
    <h2 class="text-2xl font-semibold mb-6 text-center">预约时间</h2>
    <form @submit.prevent="submitAppointment">
      <div class="mb-4">
        <label class="block mb-1 text-gray-700">姓名</label>
        <input v-model="form.name" type="text" class="w-full p-2 border rounded" required />
      </div>
      <div class="mb-4">
        <label class="block mb-1 text-gray-700">预约日期</label>
        <input v-model="form.date" type="date" class="w-full p-2 border rounded" required />
      </div>
      <div class="mb-4">
        <label class="block mb-1 text-gray-700">时间段</label>
        <select v-model="form.timeSlot" class="w-full p-2 border rounded" required>
          <option disabled value="">请选择时间段</option>
          <option>09:00 - 10:00</option>
          <option>10:00 - 11:00</option>
          <option>13:00 - 14:00</option>
          <option>15:00 - 16:00</option>
        </select>
      </div>
      <button type="submit" class="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700">
        提交预约
      </button>
    </form>

    <div v-if="submitted" class="mt-4 p-3 bg-green-100 text-green-800 rounded">
      预约提交成功！
    </div>
  </div>
</template>

<script>
export default {
  name: 'Appointment',
  data() {
    return {
      form: {
        name: '',
        date: '',
        timeSlot: '',
      },
      submitted: false,
    };
  },
  methods: {
    submitAppointment() {
      // 模拟提交请求
      console.log('预约信息：', this.form);
      // 你可以在这里发请求，例如 axios.post(...)
      this.submitted = true;

      // 清空表单（可选）
      setTimeout(() => {
        this.form = { name: '', date: '', timeSlot: '' };
        this.submitted = false;
      }, 3000);
    },
  },
};
</script>

<style scoped>
</style>
