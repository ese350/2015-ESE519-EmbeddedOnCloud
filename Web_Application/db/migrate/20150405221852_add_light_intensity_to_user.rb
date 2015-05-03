class AddLightIntensityToUser < ActiveRecord::Migration
  def change
    add_column :users, :light_intensity, :int
  end
end
