class AddLightLevelToUser < ActiveRecord::Migration
  def change
    add_column :users, :light_level, :int
  end
end
