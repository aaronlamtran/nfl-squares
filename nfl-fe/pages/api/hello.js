// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
const glob = require('glob')
console.log(glob)
export default function handler(req, res) {
  res.status(200).json({ name: 'John Doe' })
}
