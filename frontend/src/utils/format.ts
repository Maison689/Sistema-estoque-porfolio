export function formatInteger(value: number) {
  return new Intl.NumberFormat('pt-BR', {
    maximumFractionDigits: 0,
  }).format(value)
}
