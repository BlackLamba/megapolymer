import { Container } from "@/shared/ui/Container"

export const HomePage = () => {
  return (
    <Container>
      <div className="space-y-6">
        <div>
          <h1 className="text-4xl font-bold">
            Polymer Platform
          </h1>

          <p className="text-zinc-400 mt-2">
            Intelligent inverse design system for polymer materials
          </p>
        </div>

        <div className="grid grid-cols-3 gap-6">
          <div className="bg-zinc-800 rounded-2xl p-6">
            <h2 className="text-lg font-semibold">
              Generated Molecules
            </h2>

            <p className="text-4xl font-bold mt-4">
              0
            </p>
          </div>

          <div className="bg-zinc-800 rounded-2xl p-6">
            <h2 className="text-lg font-semibold">
              Experiments
            </h2>

            <p className="text-4xl font-bold mt-4">
              0
            </p>
          </div>

          <div className="bg-zinc-800 rounded-2xl p-6">
            <h2 className="text-lg font-semibold">
              Model Accuracy
            </h2>

            <p className="text-4xl font-bold mt-4">
              92%
            </p>
          </div>
        </div>
      </div>
    </Container>
  )
}