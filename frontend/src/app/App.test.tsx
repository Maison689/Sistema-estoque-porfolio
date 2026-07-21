import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { beforeEach, expect, test, vi } from 'vitest'
import { App } from './App'

const adminUser = {
  email: 'admin@example.com',
  id: 1,
  is_active: true,
  name: 'Admin User',
  role: 'ADMIN',
}

const operatorUser = {
  email: 'operator@example.com',
  id: 2,
  is_active: true,
  name: 'Operator User',
  role: 'OPERATOR',
}

beforeEach(() => {
  window.localStorage.clear()
  vi.restoreAllMocks()
})

function mockFetchForUser(user = adminUser) {
  const categories = [
    {
      description: 'Itens de tecnologia',
      id: 10,
      is_active: true,
      name: 'Informatica',
    },
  ]
  const products = [
    {
      category_id: 10,
      category_name: 'Informatica',
      id: 20,
      is_active: true,
      is_below_minimum: true,
      minimum_stock: '5.000',
      name: 'Mouse sem fio',
      quantity: '0.000',
      sku: 'MS-001',
      unit: 'UN',
    },
  ]
  const suppliers: Array<{
    email: string | null
    id: number
    is_active: boolean
    name: string
    phone: string | null
    products_count: number
    tax_id: string | null
  }> = [
    {
      email: 'contato@alpha.com',
      id: 30,
      is_active: true,
      name: 'Fornecedor Alpha',
      phone: '(11) 99999-0000',
      products_count: 1,
      tax_id: '12.345.678/0001-95',
    },
  ]
  const productSupplierLinks: Array<{
    product_id: number
    supplier_email: string | null
    supplier_id: number
    supplier_name: string
    supplier_phone: string | null
    supplier_tax_id: string | null
  }> = [
    {
      product_id: 20,
      supplier_email: 'contato@alpha.com',
      supplier_id: 30,
      supplier_name: 'Fornecedor Alpha',
      supplier_phone: '(11) 99999-0000',
      supplier_tax_id: '12.345.678/0001-95',
    },
  ]

  vi.spyOn(window, 'fetch').mockImplementation((input, init) => {
    const url = String(input)
    if (url.endsWith('/auth/login')) {
      return Promise.resolve(jsonResponse({ access_token: 'token', token_type: 'bearer' }))
    }
    if (url.endsWith('/auth/me')) {
      return Promise.resolve(jsonResponse(user))
    }
    if (url.endsWith('/auth/logout')) {
      return Promise.resolve(jsonResponse({ status: 'ok' }))
    }
    if (url.endsWith('/users')) {
      const authorization = new Headers(init?.headers).get('Authorization')
      if (!authorization) return Promise.resolve(jsonResponse({}, 401))
      return Promise.resolve(jsonResponse([adminUser]))
    }
    if (url.includes('/categories')) {
      const authorization = new Headers(init?.headers).get('Authorization')
      if (!authorization) return Promise.resolve(jsonResponse({}, 401))
      if (init?.method === 'POST') {
        categories.push({
          description: 'Itens de escritorio',
          id: 11,
          is_active: true,
          name: 'Escritorio',
        })
        return Promise.resolve(jsonResponse(categories.at(-1), 201))
      }
      if (init?.method === 'PATCH') {
        return Promise.resolve(jsonResponse({ ...categories[0], is_active: false }))
      }
      return Promise.resolve(jsonResponse(categories))
    }
    if (url.includes('/products/') && url.includes('/suppliers')) {
      const authorization = new Headers(init?.headers).get('Authorization')
      if (!authorization) return Promise.resolve(jsonResponse({}, 401))
      if (init?.method === 'POST') {
        productSupplierLinks.push({
          product_id: 20,
          supplier_email: 'beta@fornecedor.com',
          supplier_id: 31,
          supplier_name: 'Fornecedor Beta',
          supplier_phone: null,
          supplier_tax_id: null,
        })
        return Promise.resolve(jsonResponse(productSupplierLinks.at(-1), 201))
      }
      if (init?.method === 'DELETE') {
        productSupplierLinks.pop()
        return Promise.resolve(new Response(null, { status: 204 }))
      }
      return Promise.resolve(jsonResponse(productSupplierLinks))
    }
    if (url.includes('/products')) {
      const authorization = new Headers(init?.headers).get('Authorization')
      if (!authorization) return Promise.resolve(jsonResponse({}, 401))
      if (init?.method === 'POST') {
        products.push({
          category_id: 10,
          category_name: 'Informatica',
          id: 21,
          is_active: true,
          is_below_minimum: true,
          minimum_stock: '2.000',
          name: 'Teclado mecanico',
          quantity: '0.000',
          sku: 'TEC-001',
          unit: 'UN',
        })
        return Promise.resolve(jsonResponse(products.at(-1), 201))
      }
      if (init?.method === 'PATCH') {
        return Promise.resolve(jsonResponse({ ...products[0], is_active: false }))
      }
      return Promise.resolve(jsonResponse(products))
    }
    if (url.includes('/suppliers')) {
      const authorization = new Headers(init?.headers).get('Authorization')
      if (!authorization) return Promise.resolve(jsonResponse({}, 401))
      if (init?.method === 'POST') {
        suppliers.push({
          email: 'beta@fornecedor.com',
          id: 31,
          is_active: true,
          name: 'Fornecedor Beta',
          phone: null,
          products_count: 0,
          tax_id: null,
        })
        return Promise.resolve(jsonResponse(suppliers.at(-1), 201))
      }
      if (init?.method === 'PATCH') {
        return Promise.resolve(jsonResponse({ ...suppliers[0], is_active: false }))
      }
      return Promise.resolve(jsonResponse(suppliers))
    }
    if (url.endsWith('/health')) {
      return Promise.resolve(jsonResponse({ status: 'ok', service: 'Sis Estoque' }))
    }

    return Promise.resolve(jsonResponse({}, 404))
  })
}

function jsonResponse(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    headers: { 'Content-Type': 'application/json' },
    status,
  })
}

async function loginAsAdmin() {
  mockFetchForUser()
  render(<App />)

  fireEvent.change(screen.getByLabelText(/e-mail/i), {
    target: { value: 'admin@example.com' },
  })
  fireEvent.change(screen.getByLabelText(/senha/i), {
    target: { value: 'strong-password' },
  })
  fireEvent.click(screen.getByRole('button', { name: /entrar/i }))

  await waitFor(() =>
    expect(screen.getByRole('heading', { name: /dashboard/i })).toBeVisible(),
  )
}

test('logs in and renders the dashboard shell', async () => {
  await loginAsAdmin()

  expect(
    screen.getByRole('navigation', { name: /navegacao principal/i }),
  ).toBeVisible()
  expect(screen.getByText('Admin User')).toBeVisible()
  expect(screen.getByText('Produtos ativos')).toBeVisible()
})

test('navigates to admin users screen', async () => {
  await loginAsAdmin()

  fireEvent.click(screen.getByRole('button', { name: /usuarios/i }))

  await waitFor(() =>
    expect(screen.getByRole('heading', { name: /^usuarios$/i })).toBeVisible(),
  )
  expect(screen.getByText('admin@example.com')).toBeVisible()
})

test('operator does not see dashboard or users navigation', async () => {
  mockFetchForUser(operatorUser)
  render(<App />)

  fireEvent.change(screen.getByLabelText(/e-mail/i), {
    target: { value: 'operator@example.com' },
  })
  fireEvent.change(screen.getByLabelText(/senha/i), {
    target: { value: 'strong-password' },
  })
  fireEvent.click(screen.getByRole('button', { name: /entrar/i }))

  await waitFor(() =>
    expect(
      screen.getByRole('heading', { name: /catalogo de produtos/i }),
    ).toBeVisible(),
  )

  expect(screen.queryByRole('button', { name: /dashboard/i })).toBeNull()
  expect(screen.queryByRole('button', { name: /usuarios/i })).toBeNull()
  expect(screen.queryByRole('button', { name: /salvar produto/i })).toBeNull()

  fireEvent.click(screen.getByRole('button', { name: /fornecedores/i }))

  await waitFor(() =>
    expect(screen.getAllByText('Fornecedor Alpha')[0]).toBeVisible(),
  )
  expect(screen.queryByRole('button', { name: /salvar fornecedor/i })).toBeNull()
})

test('loads products and creates catalog records for admin', async () => {
  await loginAsAdmin()

  fireEvent.click(screen.getByRole('button', { name: /produtos/i }))

  await waitFor(() => expect(screen.getByText('Mouse sem fio')).toBeVisible())

  fireEvent.change(screen.getAllByLabelText(/^nome$/i)[0], {
    target: { value: 'Escritorio' },
  })
  fireEvent.click(screen.getByRole('button', { name: /salvar categoria/i }))

  await waitFor(() => expect(screen.getAllByText('Escritorio')[0]).toBeVisible())

  fireEvent.change(screen.getAllByLabelText(/^nome$/i)[1], {
    target: { value: 'Teclado mecanico' },
  })
  fireEvent.change(screen.getByLabelText(/sku/i), {
    target: { value: 'TEC-001' },
  })
  fireEvent.change(screen.getAllByLabelText(/^categoria$/i)[1], {
    target: { value: '10' },
  })
  fireEvent.change(screen.getByLabelText(/estoque minimo/i), {
    target: { value: '2.000' },
  })
  fireEvent.click(screen.getByRole('button', { name: /salvar produto/i }))

  await waitFor(() => expect(screen.getByText('Teclado mecanico')).toBeVisible())
})

test('renders required interface states after login', async () => {
  await loginAsAdmin()

  fireEvent.click(screen.getByRole('button', { name: /estados/i }))

  expect(screen.getByText('Carregando dados')).toBeVisible()
  expect(screen.getByText('Nenhum registro encontrado')).toBeVisible()
  expect(screen.getByText('Nao foi possivel carregar')).toBeVisible()
  expect(screen.getByText('Acesso negado')).toBeVisible()
})

test('loads suppliers and creates supplier links for admin', async () => {
  await loginAsAdmin()

  fireEvent.click(screen.getByRole('button', { name: /fornecedores/i }))

  await waitFor(() =>
    expect(screen.getAllByText('Fornecedor Alpha')[0]).toBeVisible(),
  )

  fireEvent.change(screen.getByLabelText(/^nome$/i), {
    target: { value: 'Fornecedor Beta' },
  })
  fireEvent.change(screen.getByLabelText(/e-mail/i), {
    target: { value: 'beta@fornecedor.com' },
  })
  fireEvent.click(screen.getByRole('button', { name: /salvar fornecedor/i }))

  await waitFor(() =>
    expect(screen.getAllByText('Fornecedor Beta')[0]).toBeVisible(),
  )

  fireEvent.change(screen.getByLabelText(/^produto$/i), {
    target: { value: '20' },
  })
  fireEvent.change(screen.getByLabelText(/^fornecedor$/i), {
    target: { value: '31' },
  })
  fireEvent.click(screen.getByRole('button', { name: /vincular fornecedor/i }))

  await waitFor(() =>
    expect(screen.getAllByText('Fornecedor Beta')[0]).toBeVisible(),
  )
})
