import { useEffect, useState } from "react"
import { getExperiment } from "@/shared/api/experiments"

import type { Experiment } from "@/shared/api/experiments"

export const useExperimentPolling = (id: number | null) => {
  const [data, setData] = useState<Experiment | null>(null)

  useEffect(() => {
    if (!id) return

    let interval: any

    const fetchData = async () => {
      try {
        const res = await getExperiment(id)
        setData(res)

        if (res.status === "done" || res.status === "failed") {
          clearInterval(interval)
        }
      } catch (e) {
        console.error(e)
      }
    }

    fetchData()
    interval = setInterval(fetchData, 1500)

    return () => clearInterval(interval)
  }, [id])

  return data
}