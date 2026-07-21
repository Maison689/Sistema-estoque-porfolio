import { useCallback, useEffect, useMemo, useState } from 'react'
import {
  createCategory,
  createProduct,
  listCategories,
  listProducts,
  updateCategory,
  updateProduct,
  type ProductFilters,
} from '../../services/inventoryService'
import { type CurrentUser } from '../../types/auth'
import {
  type Category,
  type Product,
  type ProductPayload,
  type ProductUnit,
} from '../../types/inventory'

const units: ProductUnit[] = ['UN', 'CX', 'KG', 'G', 'L', 'ML', 'M', 'CM']

type ProductsViewProps = {
  token: string
  user: CurrentUser
}

type ProductFormState = {
  categoryId: string
  minimumStock: string
  name: string
  sku: string
  unit: ProductUnit
}

const emptyProductForm: ProductFormState = {
  categoryId: '',
  minimumStock: '0.000',
  name: '',
  sku: '',
  unit: 'UN',
}

export function ProductsView({ token, user }: ProductsViewProps) {
  const canManage = user.role === 'ADMIN' || user.role === 'MANAGER'
  const [categories, setCategories] = useState<Category[]>([])
  const [products, setProducts] = useState<Product[]>([])
  const [filters, setFilters] = useState<ProductFilters>({})
  const [categoryName, setCategoryName] = useState('')
  const [categoryDescription, setCategoryDescription] = useState('')
  const [editingProductId, setEditingProductId] = useState<number | null>(null)
  const [form, setForm] = useState<ProductFormState>(emptyProductForm)
  const [isLoading, setIsLoading] = useState(true)
  const [isSaving, setIsSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const activeCategories = useMemo(
    () => categories.filter((category) => category.is_active),
    [categories],
  )

  const refreshCatalog = useCallback(async (nextFilters: ProductFilters = {}) => {
    setIsLoading(true)
    setError(null)
    try {
      const [categoryResult, productResult] = await Promise.all([
        listCategories(token),
        listProducts(token, nextFilters),
      ])
      setCategories(categoryResult)
      setProducts(productResult)
    } catch {
      setError('Nao foi possivel carregar categorias e produtos.')
    } finally {
      setIsLoading(false)
    }
  }, [token])

  useEffect(() => {
    refreshCatalog()
  }, [refreshCatalog])

  async function handleFilterChange(nextFilters: ProductFilters) {
    setFilters(nextFilters)
    await refreshCatalog(nextFilters)
  }

  async function handleCategorySubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (!canManage || !categoryName.trim()) return
    setIsSaving(true)
    setError(null)
    try {
      await createCategory(token, {
        description: categoryDescription.trim() || null,
        name: categoryName,
      })
      setCategoryName('')
      setCategoryDescription('')
      await refreshCatalog()
    } catch {
      setError('Nao foi possivel salvar a categoria.')
    } finally {
      setIsSaving(false)
    }
  }

  async function handleProductSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (!canManage || !form.categoryId) return
    setIsSaving(true)
    setError(null)
    const payload: ProductPayload = {
      category_id: Number(form.categoryId),
      minimum_stock: form.minimumStock,
      name: form.name,
      sku: form.sku,
      unit: form.unit,
    }

    try {
      if (editingProductId) {
        await updateProduct(token, editingProductId, payload)
      } else {
        await createProduct(token, payload)
      }
      setEditingProductId(null)
      setForm(emptyProductForm)
      await refreshCatalog()
    } catch {
      setError('Nao foi possivel salvar o produto.')
    } finally {
      setIsSaving(false)
    }
  }

  async function handleCategoryStatus(category: Category) {
    if (!canManage) return
    setIsSaving(true)
    setError(null)
    try {
      await updateCategory(token, category.id, { is_active: !category.is_active })
      await refreshCatalog()
    } catch {
      setError('Nao foi possivel alterar o status da categoria.')
    } finally {
      setIsSaving(false)
    }
  }

  async function handleProductStatus(product: Product) {
    if (!canManage) return
    setIsSaving(true)
    setError(null)
    try {
      await updateProduct(token, product.id, { is_active: !product.is_active })
      await refreshCatalog()
    } catch {
      setError('Nao foi possivel alterar o status do produto.')
    } finally {
      setIsSaving(false)
    }
  }

  function startProductEdit(product: Product) {
    setEditingProductId(product.id)
    setForm({
      categoryId: String(product.category_id),
      minimumStock: product.minimum_stock,
      name: product.name,
      sku: product.sku,
      unit: product.unit,
    })
  }

  return (
    <div className="page-stack">
      <section className="toolbar-panel">
        <label>
          Buscar produto
          <input
            onChange={(event) =>
              handleFilterChange({ ...filters, search: event.target.value })
            }
            placeholder="Nome ou SKU"
            type="search"
            value={filters.search ?? ''}
          />
        </label>
        <label>
          Categoria
          <select
            onChange={(event) =>
              handleFilterChange({ ...filters, categoryId: event.target.value })
            }
            value={filters.categoryId ?? ''}
          >
            <option value="">Todas</option>
            {categories.map((category) => (
              <option key={category.id} value={category.id}>
                {category.name}
              </option>
            ))}
          </select>
        </label>
        <label>
          Status
          <select
            onChange={(event) =>
              handleFilterChange({ ...filters, stockStatus: event.target.value })
            }
            value={filters.stockStatus ?? ''}
          >
            <option value="">Todos</option>
            <option value="within_minimum">Dentro do minimo</option>
            <option value="below_minimum">Abaixo do minimo</option>
          </select>
        </label>
        <button disabled={isLoading} onClick={() => refreshCatalog()} type="button">
          Atualizar
        </button>
      </section>

      {error && <p className="form-error">{error}</p>}

      {canManage && (
        <section className="split-grid">
          <form className="panel form-panel" onSubmit={handleCategorySubmit}>
            <div className="section-heading">
              <div>
                <p className="eyebrow">Categorias</p>
                <h2>Nova categoria</h2>
              </div>
            </div>
            <div className="form-grid">
              <label>
                Nome
                <input
                  onChange={(event) => setCategoryName(event.target.value)}
                  required
                  value={categoryName}
                />
              </label>
              <label>
                Descricao
                <textarea
                  onChange={(event) => setCategoryDescription(event.target.value)}
                  rows={3}
                  value={categoryDescription}
                />
              </label>
              <button disabled={isSaving} type="submit">
                Salvar categoria
              </button>
            </div>
          </form>

          <form className="panel form-panel" onSubmit={handleProductSubmit}>
            <div className="section-heading">
              <div>
                <p className="eyebrow">Produtos</p>
                <h2>{editingProductId ? 'Editar produto' : 'Novo produto'}</h2>
              </div>
            </div>
            <div className="form-grid form-grid--two">
              <label>
                Nome
                <input
                  onChange={(event) => setForm({ ...form, name: event.target.value })}
                  required
                  value={form.name}
                />
              </label>
              <label>
                SKU
                <input
                  onChange={(event) => setForm({ ...form, sku: event.target.value })}
                  required
                  value={form.sku}
                />
              </label>
              <label>
                Categoria
                <select
                  onChange={(event) =>
                    setForm({ ...form, categoryId: event.target.value })
                  }
                  required
                  value={form.categoryId}
                >
                  <option value="">Selecione</option>
                  {activeCategories.map((category) => (
                    <option key={category.id} value={category.id}>
                      {category.name}
                    </option>
                  ))}
                </select>
              </label>
              <label>
                Unidade
                <select
                  onChange={(event) =>
                    setForm({ ...form, unit: event.target.value as ProductUnit })
                  }
                  value={form.unit}
                >
                  {units.map((unit) => (
                    <option key={unit} value={unit}>
                      {unit}
                    </option>
                  ))}
                </select>
              </label>
              <label>
                Estoque minimo
                <input
                  min="0"
                  onChange={(event) =>
                    setForm({ ...form, minimumStock: event.target.value })
                  }
                  required
                  step="0.001"
                  type="number"
                  value={form.minimumStock}
                />
              </label>
              <div className="action-row action-row--end">
                {editingProductId && (
                  <button
                    onClick={() => {
                      setEditingProductId(null)
                      setForm(emptyProductForm)
                    }}
                    type="button"
                  >
                    Cancelar
                  </button>
                )}
                <button disabled={isSaving || activeCategories.length === 0} type="submit">
                  Salvar produto
                </button>
              </div>
            </div>
          </form>
        </section>
      )}

      <section className="panel">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Catalogo</p>
            <h2>Produtos cadastrados</h2>
          </div>
        </div>
        {isLoading ? (
          <div className="state-panel">
            <strong>Carregando dados</strong>
            <div className="loading-bar" />
          </div>
        ) : products.length === 0 ? (
          <div className="state-panel">
            <strong>Nenhum registro encontrado</strong>
            <p>Cadastre categorias e produtos para iniciar o catalogo.</p>
          </div>
        ) : (
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>SKU</th>
                  <th>Nome</th>
                  <th>Categoria</th>
                  <th className="align-right">Saldo</th>
                  <th className="align-right">Minimo</th>
                  <th>Status</th>
                  {canManage && <th>Acoes</th>}
                </tr>
              </thead>
              <tbody>
                {products.map((product) => (
                  <tr key={product.id}>
                    <td>{product.sku}</td>
                    <td>{product.name}</td>
                    <td>{product.category_name}</td>
                    <td className="align-right">
                      {product.quantity} {product.unit}
                    </td>
                    <td className="align-right">{product.minimum_stock}</td>
                    <td>
                      <span
                        className={
                          product.is_below_minimum
                            ? 'status-pill status-pill--warning'
                            : 'status-pill status-pill--success'
                        }
                      >
                        {product.is_active ? 'Ativo' : 'Inativo'}
                      </span>
                    </td>
                    {canManage && (
                      <td>
                        <div className="inline-actions">
                          <button onClick={() => startProductEdit(product)} type="button">
                            Editar
                          </button>
                          <button
                            onClick={() => handleProductStatus(product)}
                            type="button"
                          >
                            {product.is_active ? 'Inativar' : 'Ativar'}
                          </button>
                        </div>
                      </td>
                    )}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>

      <section className="panel">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Categorias</p>
            <h2>Categorias cadastradas</h2>
          </div>
        </div>
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Nome</th>
                <th>Descricao</th>
                <th>Status</th>
                {canManage && <th>Acoes</th>}
              </tr>
            </thead>
            <tbody>
              {categories.map((category) => (
                <tr key={category.id}>
                  <td>{category.name}</td>
                  <td>{category.description ?? '-'}</td>
                  <td>{category.is_active ? 'Ativa' : 'Inativa'}</td>
                  {canManage && (
                    <td>
                      <button
                        onClick={() => handleCategoryStatus(category)}
                        type="button"
                      >
                        {category.is_active ? 'Inativar' : 'Ativar'}
                      </button>
                    </td>
                  )}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  )
}
