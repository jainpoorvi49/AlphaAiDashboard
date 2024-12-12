import React from 'react'

const page = () => {
  return (
    <div>We are in: | {process.env.NEXT_PUBLIC_MODE}</div>
  )
}

export default page