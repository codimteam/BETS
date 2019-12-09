var cart=[]

		function Bet(ev_id,ev_time,ev_name,ev_choice,ev_coff){
			this.ev_id=ev_id;
			this.ev_time=ev_time;
			this.ev_name=ev_name;
			this.ev_choice=ev_choice;
			this.ev_coff=ev_coff;
		}

		function actInCart(id,choice,button){
			for(i=0;i<cart.length;i++){
				if(cart[i].ev_id==id&&cart[i].ev_choice==choice){
					deleteFromCart(id,choice);
					return;
				}
			}
			addToCart(id,choice,button);
		}

		function addToCart(id,choice,button){
			event_html=button.parentElement.parentElement;

			time=event_html.parentElement.getElementsByClassName('event-time')[0].innerHTML;
			var name=event_html.getElementsByClassName('team1')[0].innerHTML+" vs "
			+event_html.getElementsByClassName('team2')[0].innerHTML;
			coff=button.innerHTML;

			var bet=new Bet(id,time,name,choice,coff);
			cart.push(bet);
			saveCart();
			showCart();
		}


		function createBlock(bet){
			var newEvent=document.createElement("LI");

			var	event_teams=document.createElement('p');
			event_teams.className='event_teams';
			event_teams.innerHTML=bet.ev_name;

			var event_time=document.createElement('p');
			event_time.className='event_time';
			event_time.innerHTML=bet.ev_time;

			var topBlock=document.createElement('div');
			topBlock.className='topBlock';
			topBlock.appendChild(event_teams);
			topBlock.appendChild(event_time);



			var choice_coff=document.createElement('p');
			choice_coff.className="choice_coff";
			choice_coff.innerHTML=bet.ev_coff;

			var choice=document.createElement('p');
			choice.className='choice';
			choice.innerHTML=bet.ev_choice;

			var remove_choice=document.createElement('p');
			remove_choice.className='remove_choice';
			remove_choice.innerHTML='x';
			remove_choice.onclick=function(){
			deleteFromCart(bet.ev_id,bet.ev_choice)};

			var botBlock=document.createElement('div');
			botBlock.className='botBlock';
			botBlock.appendChild(choice);
			botBlock.appendChild(choice_coff);

			botBlock.appendChild(remove_choice);

            var submCash=document.createElement("input");
            submCash.className="submCash";
            submCash.type="number";


			var submB=document.createElement('button');
			submB.setAttribute("data-id", bet.ev_id);
			submB.setAttribute("data-choice", bet.ev_choice);
			submB.setAttribute("data-coff",bet.ev_coff);

    		submB.className="submB";
    		submB.innerHTML="make a bet";



            var submDiv=document.createElement("div");
            submDiv.appendChild(submCash);
            submDiv.appendChild(submB);
            submDiv.className="submDiv";

			newEvent.appendChild(topBlock);
			newEvent.appendChild(botBlock);
			newEvent.appendChild(submDiv);

			document.getElementById("cart").appendChild(newEvent);
		}

		function deleteFromCart(id,choice){
			for(var i=0;i<cart.length;i++){
				if(cart[i].ev_id==id&&cart[i].ev_choice==choice){
					cart.splice(i,1);
				}
			}
			saveCart();
			showCart();
		}


		function showCart(){
			document.getElementById('cart').innerHTML="";
			for(var i=0;i<cart.length;i++){
				var betBlock=createBlock(cart[i]);
			}



		}

		function loadCart(){
			cart=JSON.parse(sessionStorage.getItem('cart'));
		}

		function saveCart(){
			sessionStorage.setItem('cart',JSON.stringify(cart));
		}

		if(sessionStorage.getItem('cart')!=null){
			loadCart();
			showCart();
			// var buttons=document.getElementsByClassName("submB");
			// for(i=0;i<buttons.length;i++){
			// 	buttons[i].onclick=dothis();
			// }
		}
		// function dothis(){
		// 	alert('yess');
		// }
		$('#cart').on("click", ".submB", function(event) {
			var id=$(this).data("id");
			var choice=$(this).data("choice");
			var coff=$(this).data("coff");
			var cash=this.parentElement.getElementsByClassName('submCash')[0].value;

			var cartForm=document.getElementById("cartForm");
			var inputs=cartForm.getElementsByTagName("input");

			inputs[1].value=id;
			inputs[2].value=choice;
			inputs[3].value=coff;
			inputs[4].value=cash;
			console.log(cartForm.getElementsByTagName("input")[1].value);
			console.log(cartForm.getElementsByTagName("input")[2].value);
			console.log(cartForm.getElementsByTagName("input")[3].value);
			console.log(cartForm.getElementsByTagName("input")[4].value);
			inputs[5].click();

			deleteFromCart(bet.ev_id,bet.ev_choice);
		})
//		$('#cart').on('click','.remove_choice',deleteFromCart(event))
