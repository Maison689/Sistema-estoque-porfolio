export const dashboardMetrics = [
  { label: 'Produtos ativos', value: '128', tone: 'default' as const },
  { label: 'Abaixo do minimo', value: '9', tone: 'warning' as const },
  { label: 'Movimentacoes hoje', value: '24', tone: 'success' as const },
  { label: 'Fornecedores ativos', value: '18', tone: 'default' as const },
]

export const lowStockRows = [
  { product: 'Toner HP Laser Jet', sku: 'TON-HP-7742', quantity: '8', status: 'Abaixo' },
  { product: 'Mouse sem fio', sku: 'MOU-LOG-1290', quantity: '0', status: 'Critico' },
  { product: 'Cabo HDMI 2m', sku: 'CAB-HDMI-3321', quantity: '6', status: 'Abaixo' },
]

export const productRows = [
  { sku: 'MON-ULTRA-34', name: 'Monitor UltraWide 34', category: 'Informatica', quantity: '42', status: 'Dentro' },
  { sku: 'TON-HP-7742', name: 'Toner HP Laser Jet', category: 'Escritorio', quantity: '8', status: 'Abaixo' },
  { sku: 'CHA-PRO-8831', name: 'Cadeira ergonomica Pro', category: 'Mobiliario', quantity: '15', status: 'Dentro' },
]

export const movementRows = [
  { date: '20/07/2026 14:32', type: 'Entrada', product: 'Monitor UltraWide 34', quantity: '+12', user: 'Maria Santos' },
  { date: '20/07/2026 11:08', type: 'Saida', product: 'Toner HP Laser Jet', quantity: '-4', user: 'Ricardo Silva' },
  { date: '19/07/2026 16:10', type: 'Ajuste', product: 'Mouse sem fio', quantity: '+2', user: 'Ana Oliveira' },
]

export const supplierRows = [
  { name: 'Tecnologia Catarinense', document: 'CNPJ informado', contact: 'sac@teccat.com', products: '3' },
  { name: 'Distribuidora Ferramentas', document: 'CNPJ informado', contact: 'mendes@distriferr.com', products: '2' },
  { name: 'Alimentos Mundiais S.A.', document: 'CNPJ informado', contact: 'contato@almundi.com', products: '1' },
]
