import React from 'react'
import Deliverylist from './Deliverylist'

export default function Deliverydata() {

    const data =[
        {
            id : 1,
            name : "haha1",
            phone : "haha11",
            photo : "photu.png"
        },
        {
            id : 2,
            name : "haha2",
            phone : "haha12",
            photo : "photu.png"
        },
        {
            id : 3,
            name : "haha3",
            phone : "haha13",
            photo : "photu"
        },
        {
            id : 4,
            name : "haha4",
            phone : "haha14",
            photo : "photu.png"
        },
    ]

  return (
    <div>
        <Deliverylist data={data}/>
    </div>
  )
}
