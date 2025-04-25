import React from 'react';
import './Tile.css';

function Tile({ item, onClick, isBusiness }) {
  return (
    <div
      className={`tile ${isBusiness ? 'business-tile' : 'user-tile'}`}
      onClick={() => onClick(item)}
    >
      <h4>{item.name}</h4>
      {isBusiness ? <p>{item.address}</p> : <p>Reviews: {item.review_count}</p>}
    </div>
  );
}

export default Tile;
