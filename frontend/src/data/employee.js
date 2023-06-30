import router from '@/router'
import { createResource, createDocumentResource } from 'frappe-ui'

export const employeeResource = createDocumentResource({
  url: 'ess.api.employee.get_employee_from_user',
  cache: 'Employee',
  onError(error) {
    if (error && error.exc_type === 'AuthenticationError') {
      router.push({ name: 'app' })
    }
  },
})
