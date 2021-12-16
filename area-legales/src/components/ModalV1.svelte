<div id="topModal">
	<div id="modal">
		<div id="modal-content" style="width: 500px">
			<slot></slot>
		</div>
	</div>
</div>


<style scoped>
	#topModal {
	  z-index: 9999;
	  position: fixed;
	  top: 0;
	  left: 0;
	  right: 0;
	  bottom: 0;
	  background: #4448;
	  display: flex;
	  align-items: center;
	  justify-content: center;
	}
	#modal {
	  position: relative;
	  border-radius: 6px;
	  background: white;
      border: 2px solid #000;
	  filter: drop-shadow(5px 5px 5px #555);
	  padding: 1em;
	}
	#modal-content {
	  max-width: calc(100vw - 20px);
	  max-height: calc(100vh - 20px);
	  overflow: auto;
    }
</style>