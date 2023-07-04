const { createApp } = Vue

  createApp({
    data() {
      return {
        url:"http://127.0.0.1:5000/productos",
        productos:[],
        error:false,
        cargando:true
      }
    },
    // Se llama después de que la instancia haya 
    // terminado de procesar todas las opciones relacionadas con el estado.
    created() {
        this.fetchData(this.url)
    },
    methods: {
        fetchData(url) {
            // Acá se consume la Api
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    this.productos = data;
                    this.cargando=false
                })
                .catch(err => {
                    console.error(err);
                    this.error=true              
                })
        },
        // producto; es el id que necesita para buscar en la DB y eliminarlo
        eliminar(producto) {
            const url = 'http://localhost:5000/productos/' + producto;
            var options = {
                method: 'DELETE',
            }
            fetch(url, options)
                .then(res => res.text()) // or res.json()
                .then(res => {
                    alert("Eliminado correctamente")
                    location.reload();
                })
        }


    },
    



  }).mount('#app')


  function openModal() {
    var modal = document.getElementById("myModal");
    modal.style.display = "block";
  }
  
  function closeModal() {
    var modal = document.getElementById("myModal");
    modal.style.display = "none";
  }
  
  function eliminarProducto() {
    // Aquí puedes realizar la lógica para eliminar el producto
    closeModal();
  }