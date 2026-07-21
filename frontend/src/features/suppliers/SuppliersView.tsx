import { useCallback, useEffect, useMemo, useState } from 'react'
import { listProducts } from '../../services/inventoryService'
import {
  createProductSupplier,
  createSupplier,
  deleteProductSupplier,
  listProductSuppliers,
  listSuppliers,
  updateSupplier,
  type SupplierFilters,
} from '../../services/supplierService'
import { type CurrentUser } from '../../types/auth'
import { type Product } from '../../types/inventory'
import { type ProductSupplierLink, type Supplier } from '../../types/supplier'

type SuppliersViewProps = {
  token: string
  user: CurrentUser
}

type SupplierFormState = {
  email: string
  name: string
  phone: string
  taxId: string
}

const emptyForm: SupplierFormState = {
  email: '',
  name: '',
  phone: '',
  taxId: '',
}

export function SuppliersView({ token, user }: SuppliersViewProps) {
  const canManage = user.role === 'ADMIN' || user.role === 'MANAGER'
  const [suppliers, setSuppliers] = useState<Supplier[]>([])
  const [products, setProducts] = useState<Product[]>([])
  const [links, setLinks] = useState<ProductSupplierLink[]>([])
  const [filters, setFilters] = useState<SupplierFilters>({})
  const [form, setForm] = useState<SupplierFormState>(emptyForm)
  const [editingSupplierId, setEditingSupplierId] = useState<number | null>(null)
  const [selectedProductId, setSelectedProductId] = useState('')
  const [selectedSupplierId, setSelectedSupplierId] = useState('')
  const [isLoading, setIsLoading] = useState(true)
  const [isSaving, setIsSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const activeSuppliers = useMemo(
    () => suppliers.filter((supplier) => supplier.is_active),
    [suppliers],
  )
  const activeProducts = useMemo(
    () => products.filter((product) => product.is_active),
    [products],
  )

  const refreshSuppliers = useCallback(
    async (nextFilters: SupplierFilters = filters) => {
      setIsLoading(true)
      setError(null)
      try {
        const [supplierResult, productResult] = await Promise.all([
          listSuppliers(token, nextFilters),
          listProducts(token),
        ])
        setSuppliers(supplierResult)
        setProducts(productResult)
        if (!selectedProductId && productResult.length > 0) {
          setSelectedProductId(String(productResult[0].id))
        }
      } catch {
        setError('Nao foi possivel carregar fornecedores.')
      } finally {
        setIsLoading(false)
      }
    },
    [filters, selectedProductId, token],
  )

  const refreshLinks = useCallback(async () => {
    if (!selectedProductId) {
      setLinks([])
      return
    }
    try {
      setLinks(await listProductSuppliers(token, Number(selectedProductId)))
    } catch {
      setError('Nao foi possivel carregar os vinculos do produto.')
    }
  }, [selectedProductId, token])

  useEffect(() => {
    refreshSuppliers()
  }, [refreshSuppliers])

  useEffect(() => {
    refreshLinks()
  }, [refreshLinks])

  async function handleFilterChange(nextFilters: SupplierFilters) {
    setFilters(nextFilters)
    await refreshSuppliers(nextFilters)
  }

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (!canManage) return
    setIsSaving(true)
    setError(null)
    const payload = {
      email: form.email.trim() || null,
      name: form.name,
      phone: form.phone.trim() || null,
      tax_id: form.taxId.trim() || null,
    }
    try {
      if (editingSupplierId) {
        await updateSupplier(token, editingSupplierId, payload)
      } else {
        await createSupplier(token, payload)
      }
      setEditingSupplierId(null)
      setForm(emptyForm)
      await refreshSuppliers()
    } catch {
      setError('Nao foi possivel salvar o fornecedor.')
    } finally {
      setIsSaving(false)
    }
  }

  async function handleSupplierStatus(supplier: Supplier) {
    if (!canManage) return
    setIsSaving(true)
    setError(null)
    try {
      await updateSupplier(token, supplier.id, { is_active: !supplier.is_active })
      await refreshSuppliers()
      await refreshLinks()
    } catch {
      setError('Nao foi possivel alterar o status do fornecedor.')
    } finally {
      setIsSaving(false)
    }
  }

  async function handleCreateLink(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (!canManage || !selectedProductId || !selectedSupplierId) return
    setIsSaving(true)
    setError(null)
    try {
      await createProductSupplier(token, Number(selectedProductId), Number(selectedSupplierId))
      setSelectedSupplierId('')
      await refreshLinks()
      await refreshSuppliers()
    } catch {
      setError('Nao foi possivel criar o vinculo.')
    } finally {
      setIsSaving(false)
    }
  }

  async function handleRemoveLink(supplierId: number) {
    if (!canManage || !selectedProductId) return
    setIsSaving(true)
    setError(null)
    try {
      await deleteProductSupplier(token, Number(selectedProductId), supplierId)
      await refreshLinks()
      await refreshSuppliers()
    } catch {
      setError('Nao foi possivel remover o vinculo.')
    } finally {
      setIsSaving(false)
    }
  }

  function startEdit(supplier: Supplier) {
    setEditingSupplierId(supplier.id)
    setForm({
      email: supplier.email ?? '',
      name: supplier.name,
      phone: supplier.phone ?? '',
      taxId: supplier.tax_id ?? '',
    })
  }

  return (
    <div className="page-stack">
      <section className="metric-grid" aria-label="Resumo de fornecedores">
        <div className="metric-card">
          <span>Ativos</span>
          <strong>{suppliers.filter((supplier) => supplier.is_active).length}</strong>
        </div>
        <div className="metric-card metric-card--success">
          <span>Com produtos</span>
          <strong>{suppliers.filter((supplier) => supplier.products_count > 0).length}</strong>
        </div>
        <div className="metric-card metric-card--danger">
          <span>Inativos</span>
          <strong>{suppliers.filter((supplier) => !supplier.is_active).length}</strong>
        </div>
      </section>

      <section className="toolbar-panel">
        <label>
          Buscar fornecedor
          <input
            onChange={(event) =>
              handleFilterChange({ ...filters, search: event.target.value })
            }
            placeholder="Nome, documento ou e-mail"
            type="search"
            value={filters.search ?? ''}
          />
        </label>
        <label>
          Estado
          <select
            onChange={(event) =>
              handleFilterChange({ ...filters, isActive: event.target.value })
            }
            value={filters.isActive ?? ''}
          >
            <option value="">Todos</option>
            <option value="true">Ativos</option>
            <option value="false">Inativos</option>
          </select>
        </label>
        <button disabled={isLoading} onClick={() => refreshSuppliers()} type="button">
          Atualizar
        </button>
      </section>

      {error && <p className="form-error">{error}</p>}

      {canManage && (
        <section className="split-grid">
          <form className="panel form-panel" onSubmit={handleSubmit}>
            <div className="section-heading">
              <div>
                <p className="eyebrow">Fornecedores</p>
                <h2>{editingSupplierId ? 'Editar fornecedor' : 'Novo fornecedor'}</h2>
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
                CPF ou CNPJ
                <input
                  onChange={(event) => setForm({ ...form, taxId: event.target.value })}
                  value={form.taxId}
                />
              </label>
              <label>
                E-mail
                <input
                  onChange={(event) => setForm({ ...form, email: event.target.value })}
                  type="email"
                  value={form.email}
                />
              </label>
              <label>
                Telefone
                <input
                  onChange={(event) => setForm({ ...form, phone: event.target.value })}
                  value={form.phone}
                />
              </label>
              <div className="action-row action-row--end">
                {editingSupplierId && (
                  <button
                    onClick={() => {
                      setEditingSupplierId(null)
                      setForm(emptyForm)
                    }}
                    type="button"
                  >
                    Cancelar
                  </button>
                )}
                <button disabled={isSaving} type="submit">
                  Salvar fornecedor
                </button>
              </div>
            </div>
          </form>

          <form className="panel form-panel" onSubmit={handleCreateLink}>
            <div className="section-heading">
              <div>
                <p className="eyebrow">Vinculos</p>
                <h2>Produto e fornecedor</h2>
              </div>
            </div>
            <div className="form-grid">
              <label>
                Produto
                <select
                  onChange={(event) => setSelectedProductId(event.target.value)}
                  required
                  value={selectedProductId}
                >
                  <option value="">Selecione</option>
                  {activeProducts.map((product) => (
                    <option key={product.id} value={product.id}>
                      {product.name}
                    </option>
                  ))}
                </select>
              </label>
              <label>
                Fornecedor
                <select
                  onChange={(event) => setSelectedSupplierId(event.target.value)}
                  required
                  value={selectedSupplierId}
                >
                  <option value="">Selecione</option>
                  {activeSuppliers.map((supplier) => (
                    <option key={supplier.id} value={supplier.id}>
                      {supplier.name}
                    </option>
                  ))}
                </select>
              </label>
              <button disabled={isSaving || !selectedProductId} type="submit">
                Vincular fornecedor
              </button>
            </div>
          </form>
        </section>
      )}

      <section className="panel">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Fornecedores</p>
            <h2>Gestao de fornecedores</h2>
          </div>
        </div>
        {isLoading ? (
          <div className="state-panel">
            <strong>Carregando dados</strong>
            <div className="loading-bar" />
          </div>
        ) : suppliers.length === 0 ? (
          <div className="state-panel">
            <strong>Nenhum registro encontrado</strong>
            <p>Cadastre fornecedores para associar aos produtos.</p>
          </div>
        ) : (
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Empresa</th>
                  <th>Documento</th>
                  <th>Contato</th>
                  <th className="align-right">Produtos</th>
                  <th>Status</th>
                  {canManage && <th>Acoes</th>}
                </tr>
              </thead>
              <tbody>
                {suppliers.map((supplier) => (
                  <tr key={supplier.id}>
                    <td>{supplier.name}</td>
                    <td>{supplier.tax_id ?? '-'}</td>
                    <td>{supplier.email ?? supplier.phone ?? '-'}</td>
                    <td className="align-right">{supplier.products_count}</td>
                    <td>{supplier.is_active ? 'Ativo' : 'Inativo'}</td>
                    {canManage && (
                      <td>
                        <div className="inline-actions">
                          <button onClick={() => startEdit(supplier)} type="button">
                            Editar
                          </button>
                          <button onClick={() => handleSupplierStatus(supplier)} type="button">
                            {supplier.is_active ? 'Inativar' : 'Ativar'}
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
            <p className="eyebrow">Vinculos</p>
            <h2>Fornecedores do produto</h2>
          </div>
        </div>
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Fornecedor</th>
                <th>Documento</th>
                <th>Contato</th>
                {canManage && <th>Acoes</th>}
              </tr>
            </thead>
            <tbody>
              {links.length === 0 ? (
                <tr>
                  <td colSpan={canManage ? 4 : 3}>Nenhum fornecedor vinculado.</td>
                </tr>
              ) : (
                links.map((link) => (
                  <tr key={link.supplier_id}>
                    <td>{link.supplier_name}</td>
                    <td>{link.supplier_tax_id ?? '-'}</td>
                    <td>{link.supplier_email ?? link.supplier_phone ?? '-'}</td>
                    {canManage && (
                      <td>
                        <button onClick={() => handleRemoveLink(link.supplier_id)} type="button">
                          Remover
                        </button>
                      </td>
                    )}
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  )
}
