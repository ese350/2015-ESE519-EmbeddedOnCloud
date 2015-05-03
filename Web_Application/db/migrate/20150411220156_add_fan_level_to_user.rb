class AddFanLevelToUser < ActiveRecord::Migration
  def change
    add_column :users, :fan_level, :int
  end
end
