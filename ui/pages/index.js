import axios from "axios"
export default function Home({blocks}){
  return (
    <div className="p-6">
      <h1>Bytecoin Explorer</h1>
      <ul>
        {blocks.map(b => (
          <li key={b.height}>
            <a href={`/block/${b.height}`}>Height {b.height} — {b.hash}</a>
          </li>
        ))}
      </ul>
    </div>
  )
}
export async function getServerSideProps(){
  const res = await fetch("http://127.0.0.1:5000/blocks")
  const blocks = await res.json()
  return {props: {blocks}}
}
