import './MainModal.css';

import { Link } from "react-router-dom";

function MainModal() {
  return (
    <div className='main-container main-modal'>
      <nav className="navbar navbar-light bg-light">
        <div className="container-fluid">
          <div className='left-navbar'>
            <a class="navbar-brand" href="#">DEMO</a>
          </div>
          <div className='right-navbar'>
            <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal">
            Checkout
            </button>
            <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
              <div class="modal-dialog">
                <div class="modal-content">
                  <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLabel">Verify your age</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                  </div>
                  <div class="modal-body">
                    To buy the items in your cart, you need to first verify your age
                  </div>
                  <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <Link to="/cards" className="btn btn-primary">Verify Age</Link>                 
                  </div>
                </div>
              </div>
            </div>
          </div>
          
        </div>
      </nav>
     
      <div className="container2">
        <div class="p-3 mb-2 bg-secondary text-white">Your Basket</div>
        <div className='container3'>
          <div class="row">
            <div class="col-6"  style={ {border:'1px solid #cecece' }}>
              'image here'
            </div>
            <div class="col"  style={ {border:'1px solid #cecece' }}>
              'product name'
            </div>
            <div class="col"  style={ {border:'1px solid #cecece' }}>
              'price'
            </div>
            </div>
            </div>
            <div className='container4'>
          <div class="row">
            <div class="col-9" >
             
            </div>
            <div class="col"  >
              'total price'
            </div>
          </div>

        </div>
      </div>
     

    </div>
  );
}

export default MainModal;