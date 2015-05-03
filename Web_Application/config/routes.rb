Project0::Application.routes.draw do

  
  
  get 'sensors/update_temperature'

  get 'sessions/new'

  get 'users/new'

  root 'static_pages#home'
  get 'help' =>'static_pages#help'
  get 'about' => 'static_pages#about'
  get 'contact' => 'static_pages#contact'
  get 'signup' => 'users#new'
  get    'login'   => 'sessions#new'
  post   'login'   => 'sessions#create'
  delete 'logout'  => 'sessions#destroy'

  get '/update_temperature/:fn/:val' => 'sensors#update_temperature'
  get '/update_light_intensity/:fn/:val' => 'sensors#update_light_intensity'
  get '/update_humidity/:fn/:val' => 'sensors#update_humidity'
  get '/update_noise_level/:fn/:val' => 'sensors#update_noise_level'
  get '/update_pulse_rate/:fn/:val' => 'sensors#update_pulse_rate'
  get '/parameters/:fn' => 'sensors#parameters'
  get 'update_light/:fn/:val' => 'sensors#update_light'
  get 'update_fan/:fn/:val' => 'sensors#update_fan'
  resources :users

  # The priority is based upon order of creation: first created -> highest priority.
  # See how all your routes lay out with "rake routes".

  # Example of regular route:
  #   get 'products/:id' => 'catalog#view'

  # Example of named route that can be invoked with purchase_url(id: product.id)
  #   get 'products/:id/purchase' => 'catalog#purchase', as: :purchase

  # Example resource route (maps HTTP verbs to controller actions automatically):
  #   resources :products

  # Example resource route with options:
  #   resources :products do
  #     member do
  #       get 'short'
  #       post 'toggle'
  #     end
  #
  #     collection do
  #       get 'sold'
  #     end
  #   end

  # Example resource route with sub-resources:
  #   resources :products do
  #     resources :comments, :sales
  #     resource :seller
  #   end

  # Example resource route with more complex sub-resources:
  #   resources :products do
  #     resources :comments
  #     resources :sales do
  #       get 'recent', on: :collection
  #     end
  #   end

  # Example resource route with concerns:
  #   concern :toggleable do
  #     post 'toggle'
  #   end
  #   resources :posts, concerns: :toggleable
  #   resources :photos, concerns: :toggleable

  # Example resource route within a namespace:
  #   namespace :admin do
  #     # Directs /admin/products/* to Admin::ProductsController
  #     # (app/controllers/admin/products_controller.rb)
  #     resources :products
  #   end
end
