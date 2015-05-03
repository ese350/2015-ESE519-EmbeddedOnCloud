class AddHumidityToUser < ActiveRecord::Migration
  def change
    add_column :users, :humidity, :int
  end
end
