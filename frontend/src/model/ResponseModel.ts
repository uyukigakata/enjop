export interface Law {
  law_id: string
  law_name: string
  law_risk_level: number
  law_reason: string
}

export interface Response {
  laws: Law[]
  comment: string
  rating: number
}
